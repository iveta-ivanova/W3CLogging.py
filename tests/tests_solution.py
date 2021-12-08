# import pytest

from log_analysis import Logs


def test_logs():
    """
    Test if list (set) of file paths is successfully generated
    using the user-specified directory, subdirectory or file in current
    project directory. Test if non .log files are ignored.
    """
    logs = Logs(["example/dir_1", "example/example.log", "example9.log"], "cs-uri-stem")
    logs = logs.get_logs()
    assert logs == {
        "example/dir_1\\example2.log",
        "example/dir_1\\example3.log",
        "example/dir_1\\example5.log",
        "example/example.log",
        "example9.log",
    }


def test_parsing():
    """
    Test if log entries are successfully parsed and a correct
    sorted list of URI hits is generated.
    """
    logs = Logs(["example/dir_1/example3.log"], "cs-uri-stem")
    log_files = logs.get_logs()
    lines = logs.read_logs()

    assert lines == [
        "2002-05-04 17:42:15 172.22.255.255 - 172.30.255.255 80 GET /images/picture.jpg - 200 Mozilla/4.0+",
        "2002-05-04 17:30:15 172.22.255.255 - 172.30.255.255 80 GET /images/picture2.jpg - 200 Mozilla/4.0+",
        "2002-05-04 09:30:15 172.22.255.255 - 172.30.255.255 80 GET /images/picture2.jpg - 200 Mozilla/4.0+",
        "2002-05-04 10:42:15 172.22.255.255 - 172.30.255.255 80 GET /images/picture3.jpg - 200 Mozilla/4.0+",
        "2002-05-04 09:30:15 172.22.255.255 - 172.30.255.255 80 GET /images/picture3.jpg - 200 Mozilla/4.0+",
        "2002-05-04 09:30:15 172.22.255.255 - 172.30.255.255 80 GET /images/picture3.jpg - 200 Mozilla/4.0+",
    ]

    assert logs.uri_statistics == [
        ("/images/picture3.jpg", 3),
        ("/images/picture2.jpg", 2),
        ("/images/picture.jpg", 1),
    ]


def test_nofields():
    """
    Test in the event of no "#Fields" metadata in the log
    => returns empty statistics.
    """
    logs = Logs(["example/example2_nofield.log"], "cs-uri-stem")
    log_files = logs.get_logs()
    lines = logs.read_logs()

    assert logs.uri_statistics == []


def test_different_format():
    """
    Test a log file where "#Fields" follows a log entry => entries
    before the Fields metadata is ignored.
    """
    logs = Logs(["example/example2_diff_order.log"], "cs-uri-stem")
    log_files = logs.get_logs()
    lines = logs.read_logs()
    assert logs.uri_statistics == [
        ("/images/picture4.jpg", 1),
        ("/images/picture.jpg", 1),
    ]

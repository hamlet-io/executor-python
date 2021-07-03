import os
import json
import tempfile
import pytest
from hamlet.backend.common.fsutils import Search, ContextSearch, Directory, File


def test_search():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = "/test/path/split"
        assert Search.split_path(path) == ["/", "test", "path", "split"]
        path = "test/path/split"
        assert Search.split_path(path) == ["test", "path", "split"]

        test_directory_fullpath = os.path.join(temp_dir, "test/directory")
        test_directory_1_fullpath = os.path.join(temp_dir, "test/directory/1")
        test_directory_2_fullpath = os.path.join(temp_dir, "test/directory/2")
        test_filename_fullpath = os.path.join(test_directory_fullpath, "node-0")
        test_filename_1_fullpath = os.path.join(test_directory_1_fullpath, "node-1")
        test_filename_2_fullpath = os.path.join(test_directory_2_fullpath, "node-2")
        os.makedirs(test_directory_1_fullpath)
        os.makedirs(test_directory_2_fullpath)
        os.mknod(test_filename_fullpath)
        os.mknod(test_filename_1_fullpath)
        os.mknod(test_filename_2_fullpath)

        assert os.path.exists(test_filename_fullpath)
        assert os.path.exists(test_filename_1_fullpath)
        assert os.path.exists(test_filename_2_fullpath)

        with pytest.raises(ValueError):
            ContextSearch(os.path.relpath(temp_dir, test_directory_fullpath))

        with pytest.raises(ValueError):
            ContextSearch(test_filename_fullpath)

        with pytest.raises(ValueError):
            ContextSearch("/directory/doesnt/exist")

        assert (
            Search.exists(test_directory_fullpath, "node-0") == test_filename_fullpath
        )
        assert (
            ContextSearch(test_directory_fullpath).exists("node-0")
            == test_filename_fullpath
        )
        assert (
            Search.exists(test_directory_1_fullpath, "node-1")
            == test_filename_1_fullpath
        )
        assert (
            ContextSearch(test_directory_1_fullpath).exists("node-1")
            == test_filename_1_fullpath
        )
        assert (
            Search.exists(test_directory_2_fullpath, "node-2")
            == test_filename_2_fullpath
        )
        assert (
            ContextSearch(test_directory_2_fullpath).exists("node-2")
            == test_filename_2_fullpath
        )

        assert (
            Search.exists(test_directory_1_fullpath, "node-0", up=1)
            == test_filename_fullpath
        )
        assert (
            ContextSearch(test_directory_1_fullpath).exists("node-0", up=1)
            == test_filename_fullpath
        )
        assert (
            Search.exists(test_directory_2_fullpath, "node-0", up=1)
            == test_filename_fullpath
        )
        assert (
            ContextSearch(test_directory_2_fullpath).exists("node-0", up=1)
            == test_filename_fullpath
        )

        assert (
            Search.isfile(test_directory_fullpath, "node-0") == test_filename_fullpath
        )
        assert (
            ContextSearch(test_directory_fullpath).isfile("node-0")
            == test_filename_fullpath
        )

        assert (
            Search.isfile(test_directory_1_fullpath, "node-0", up=1)
            == test_filename_fullpath
        )
        assert (
            ContextSearch(test_directory_1_fullpath).isfile("node-0", up=1)
            == test_filename_fullpath
        )

        assert (
            Search.isdir(
                test_directory_fullpath, os.path.basename(test_directory_1_fullpath)
            )
            == test_directory_1_fullpath
        )
        assert (
            ContextSearch(test_directory_fullpath).isdir(
                os.path.basename(test_directory_1_fullpath)
            )
            == test_directory_1_fullpath
        )
        assert (
            Search.isdir(
                test_directory_1_fullpath,
                os.path.basename(test_directory_fullpath),
                up=2,
            )
            == test_directory_fullpath
        )
        assert (
            ContextSearch(test_directory_1_fullpath).isdir(
                os.path.basename(test_directory_fullpath), up=2
            )
            == test_directory_fullpath
        )

        assert (
            Search.upwards(test_directory_1_fullpath, "node-0")
            == test_filename_fullpath
        )
        assert (
            ContextSearch(test_directory_2_fullpath).upwards("node-0")
            == test_filename_fullpath
        )

        assert Search.downwards(temp_dir, "node-1") == [test_filename_1_fullpath]
        assert ContextSearch(temp_dir).downwards("node-2") == [test_filename_2_fullpath]

        assert Search.basename(test_directory_fullpath) == os.path.basename(
            test_directory_fullpath
        )
        assert ContextSearch(test_directory_fullpath).basename() == os.path.basename(
            test_directory_fullpath
        )

        assert Search.basename(test_directory_1_fullpath, up=1) == os.path.basename(
            test_directory_fullpath
        )
        assert ContextSearch(test_directory_2_fullpath).basename(
            up=1
        ) == os.path.basename(test_directory_fullpath)

        assert Search.parent(test_directory_1_fullpath, up=1) == test_directory_fullpath
        assert (
            ContextSearch(test_directory_2_fullpath).parent(up=1)
            == test_directory_fullpath
        )

        assert Search.parent(test_directory_1_fullpath, up=3) == temp_dir
        assert ContextSearch(test_directory_2_fullpath).parent(up=3) == temp_dir

        assert (
            Search.cut(
                "/p/re/fix/path/to/something/suf/fix",
                prefix="/p/re/fix",
                suffix="suf/fix",
            )
            == "path/to/something"
        )
        assert (
            Search.cut("/p/re/fix/path/to/something/suf/fix", prefix="/p/re/fix")
            == "path/to/something/suf/fix"
        )
        assert (
            Search.cut("/p/re/fix/path/to/something/suf/fix", suffix="suf/fix")
            == "/p/re/fix/path/to/something"
        )


def test_fs_interface():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_directory_relpath = os.path.join("test", "directory", "path")
        test_directory_fullpath = os.path.join(temp_dir, test_directory_relpath)
        test_json_file_fullpath = os.path.join(test_directory_fullpath, "test.json")
        test_text_file_fullpath = os.path.join(test_directory_fullpath, "test.txt")
        os.makedirs(test_directory_fullpath)
        with open(test_json_file_fullpath, "wt+") as f:
            data = {"data": {"key": "value"}}
            json.dump(data, f)
        with open(test_text_file_fullpath, "wt+") as f:
            f.write("Hello world!")

        directory = Directory(temp_dir)
        assert (
            directory["test"]["directory"]["path"]["test.json"]["data"]["key"]
            == "value"
        )
        with pytest.raises(KeyError):
            assert directory["test"]["directory"]["path"]["nofile.json"]
        with pytest.raises(TypeError) as einfo:
            directory["test"]["directory"]["path"]["test.txt"]["data"]
        assert str(einfo.value) == "Unstructured data"

    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(10):
            os.mknod(os.path.join(temp_dir, f"{i}-file"))
            os.mkdir(os.path.join(temp_dir, f"{i}-directory"))
        directory = Directory(temp_dir)
        c = 0
        for item in directory:
            c += 1
            if item.path.endswith("-file"):
                assert isinstance(item, File)
            elif item.path.endswith("-directory"):
                assert isinstance(item, Directory)
        assert c == 20

    with tempfile.TemporaryDirectory() as temp_dir:
        test_json_file_fullpath = os.path.join(temp_dir, "test.json")
        test_text_file_fullpath = os.path.join(temp_dir, "test.txt")
        with open(test_json_file_fullpath, "wt+") as f:
            data = {"data": {"key": "value"}}
            json.dump(data, f)
        with open(test_text_file_fullpath, "wt+") as f:
            f.write("Hello world!")

        file_interface = File(test_json_file_fullpath)
        assert file_interface["data"]["key"] == "value"
        file_interface["data"]["key"] = "modified"
        file_interface.write()
        file_interface = File(test_json_file_fullpath)
        assert file_interface["data"]["key"] == "modified"
        with open(test_json_file_fullpath, "wt+") as f:
            data = {"message": "changed"}
            json.dump(data, f)
        file_interface.reload()
        assert file_interface["message"] == "changed"

        file_interface = File(test_text_file_fullpath)
        file_interface.load()
        assert file_interface.data == "Hello world!"
        file_interface.data = "Goodbye world!"
        file_interface.write()
        file_interface = File(test_text_file_fullpath)
        file_interface.load()
        assert file_interface.data == "Goodbye world!"

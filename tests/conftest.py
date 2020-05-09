"""共通fixutureインスタンス

conftest.pyというファイル名で実装しておくことで、各テストでimportしなくても自動で利用できる。
fixutureとはテストに先立って実行される関数

fixutureについて
https://docs.pytest.org/en/latest/fixture.html
"""
import pytest
import os
import tempfile
import shutil

class SampleConnection():

    def __init__(self, name):
        super().__init__()
        self.name = name


# paramsを定義すると、パラメータ分実行される
# この定義でいうと３回。３回目はSKIPされる
@pytest.fixture(scope='session', params=['TestConnection1', 'TextConnection2', pytest.param('TestConnection3', marks=pytest.mark.skip)])
def connection(request):
    con = SampleConnection(request.param)
    return con

@pytest.fixture
def cleandir():
    print('cleardir start')
    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    print('TEMP FILE PATH:{0}'.format(newpath))
    os.chdir(newpath)
    yield 
    os.chdir(old_cwd)
    shutil.rmtree(newpath)
    print('cleardir end')


"""pytestを利用したテストサンプル
pytestはunittestで記載された内容も実行は可能
"""
import pytest
import sys
import src.pipenv_test.main as target

def teardown1():
    print('teardown1 complete')


# fixture定義を引数で取るテスト関数で有効になる。
# module単位の定義をしても引数で渡されている関数で初めて実行される
# scope定義
# default   -> テストメソッド毎に実行
# "module"  -> モジュール毎に１度実行
# "session" -> テスト全体で１度実行
@pytest.fixture(scope='module')
def con(request, connection):
    # 前処理    
    print('')
    print('PATH:{0}'.format(str(sys.path)))
    print('before yeild process complete')
    # 後処理２登録
    # finalizerは複数登録できる
    request.addfinalizer(teardown1)
    request.addfinalizer(lambda con =connection : print('teardown2 complete. connection_name:{0}'.format(con.name)))

    # テスと実行
    yield connection 

    # 後処理１
    # yieldに達する前にエラーになった場合、これ以降の処理も行われない。
    # 確実に終了処理を行うためには、コンテキストにfinalizerを追加すること
    print('')
    print('after yeild process complete')
    # finalizerよりも先に実行される。
    # オブジェクトの値を変更することが可能
    # テストケース毎にこれを実行すると、test_connection_nameがエラーとなる。
    # test_connection_name以前のテストケースの後処理によって名前が書き換わるため。
    connection.name = 'ChangedConnection'



# テストケース毎にtempディレクトリの初期化を行うなどが可能
# テストメソッド毎の設定も可能
# テスト全体で利用するのであれば、iniファイルに記載も可能
# クラス名はTest始まりでないといけない
@pytest.mark.usefixtures('cleandir')
class TestFixuture():

    def test_zero_division(self, con):
        """エラーケーステスト
        """
        with pytest.raises(ZeroDivisionError):
            1 / 0

    def test_recursion_depth(self, con):
        with pytest.raises(RuntimeError) as excinfo:
            def f():
                f()
            f()
        assert 'maximum recursion' in str(excinfo.value)


    def test_connection_name(self, con):
        assert 'TestConnection1' == con.name

@pytest.mark.usefixtures('cleandir')
def test_1(con):
    assert 1 == 1

def test_ip(con):
    assert '1.1.1.1' == target.get_ip()

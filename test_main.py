"""テストサンプル
"""
import pytest

def teardown1():
    print('teardown1 complete')

def teardown2():
    print('teardown2 complete')


# fixture定義を引数で取るテスト関数で有効になる。
# module単位の定義をしても引数で渡されている関数で初めて実行される
# scope定義
# default   -> テストメソッド毎に実行
# "module"  -> モジュール毎に１度実行
# "session" -> テスト全体で１度実行
@pytest.fixture(scope="module")
def setup(request):
    class Hoge:
        def __init__(self, value):
                super().__init__()
                self.hoge = value

        def get_hoge(self):
            return self.hoge

        def set_hoge(self, value):
            self.hoge = value
    
    print('')
    print('setup complete')
    hoge = Hoge('aaaaa')

    # finalizerは複数登録できる
    request.addfinalizer(teardown1)
    request.addfinalizer(teardown2)
    yield hoge

    # yieldに達する前にエラーになった場合、これ以降の処理も行われない。
    # 確実に終了処理を行うためには、コンテキストにfinalizerを追加すること
    print('')
    print('after yeild process complete')
    hoge.set_hoge('bbbbb')


def test_zero_division():
    """エラーケーステスト
    """
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_recursion_depth(setup):
    with pytest.raises(RuntimeError) as excinfo:
        def f():
            f()
        f()
    assert 'maximum recursion' in str(excinfo.value)

def test_setup(setup):
    assert 'aaaaa' == setup.get_hoge()

def test_1():
    assert 1 == 1

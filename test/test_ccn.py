import lizard
import pathlib
import unittest


class TestCCN(unittest.TestCase):

    def setUp(self) -> None:
        """
        初始化 lizard
        """
        self.debug = False
        self.results = []
        path = pathlib.Path(__file__).parent.parent
        for file in path.rglob("*.py"):
            if self.debug:
                print(file.absolute())
            result = lizard.analyze_file(str(file.absolute()))
            self.results.append(result)
            if self.debug:
                print("result:", result.__dict__)
                result = result.__dict__
                for func in result['function_list']:
                    print("function:", func.name)
                    print(func.__dict__)
                print("=" * 30)

    def test_nloc(self):
        """
        不带注释的代码行检查
        """
        for result in self.results:
            for func in result.function_list:
                self.assertLess(func.nloc, 100, "{}:不带注释的代码行应该小于100,但是当前是{}".format(func.name, func.nloc))
            self.assertLess(result.nloc, 100, "{}:不带注释的代码行应该小于100,但是当前是{}".format(result.filename, result.nloc))

    def test_ccn(self):
        """
        圈复杂度检查
        """
        for result in self.results:
            for func in result.function_list:
                self.assertLess(func.cyclomatic_complexity, 20,
                                "{}:圈复杂度应当小于20,但是当前是{}".format(func.name, func.cyclomatic_complexity))
            self.assertLess(result.average_cyclomatic_complexity, 10,
                            "{}:圈复杂度应当小于10,但是当前是{}".format(result.filename, result.average_cyclomatic_complexity))

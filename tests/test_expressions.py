try:
    from . import context
except:
    import context 

from  pymugen.entities.expressions import *
import unittest as ut


class MathExpTest(ut.TestCase):
    inter, parser = None, None

    def setUp(self):
        self.parser = get_parser()
        self.inter = ExpressionInterpreter()

    def tearDown(self):
        self.parser = None
        self.inter = None

    def _eval(self, exp): 
        r = self.parser.parse(exp)
        return self.inter.visit(r)

    def test_assignment(self):
        tests = (
            "a:=1","b:=2","c:=3"
        )
        for t in tests:
           self._eval(t)
        mem = self.inter._env.variables
        self.assertEqual(mem['a'], 1)
        self.assertEqual(mem['b'], 2)
        self.assertEqual(mem['c'], 3)

    def test_general(self):
        tests = (
            "1", '"ciao"',"1.1", "1+1", 
            "1+2", "((1)+(2+4))","1*5","4/3", " 1 && 0 || 1",
            "1=0", "1>0", "pippo:=PI/2", "pippo", "(sin(2*pippo) + 1) * 2",
            "(1+1)+2",
            "(1*4)", "(1+1)=(2+2)", "(2)",
            "!1","!(2-2)",
            "a:=E","sin(1)", "log(2,128)","(abs(5)) >0",
            "ciao:=1",
            "(!1)+(2*3)",
            "!1+2*3"
        )

        for t in tests:
           self._eval(t)
        mem = self.inter._env.variables
        self.assertEqual(mem['ciao'], 1)
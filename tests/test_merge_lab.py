import unittest
from merge_lab import diff,merge


class MergeLabTests(unittest.TestCase):
    def test_diff(self):
        self.assertIn("+new",diff("old\n","new\n"))
    def test_same(self):
        self.assertEqual(merge("a\n","b\n","b\n")["text"],"b\n")
    def test_only_ours(self):
        self.assertEqual(merge("a\n","b\n","a\n")["text"],"b\n")
    def test_only_theirs(self):
        self.assertEqual(merge("a\n","a\n","b\n")["text"],"b\n")
    def test_nonoverlapping(self):
        result=merge("a\nb\nc\n","A\nb\nc\n","a\nb\nC\n")
        self.assertEqual(result["text"],"A\nb\nC\n")
    def test_conflict(self):
        self.assertEqual(merge("a\n","b\n","c\n")["conflicts"],1)
    def test_no_change(self):
        self.assertEqual(merge("a\n","a\n","a\n")["text"],"a\n")
    def test_identical_change(self):
        self.assertEqual(merge("a\nb\n","A\nb\n","A\nb\n")["conflicts"],0)


if __name__=="__main__":
    unittest.main()

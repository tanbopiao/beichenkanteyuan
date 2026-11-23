"""北辰勘慝院（BEICHEN-KANTEYUAN）算子骨架单测：名帖完整、桩位齐整、只增不覆盖。"""
import unittest

from beichenkanteyuan import BeichenKanteyuan


class TestBeichenKanteyuan(unittest.TestCase):
    def setUp(self):
        self.op = BeichenKanteyuan()

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "beichenkanteyuan")
        self.assertEqual(d["code"], "BEICHEN-KANTEYUAN")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertTrue(d["mingwen"])

    def test_issue_order_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.issue_order(None, None)

    def test_pardon_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.pardon(None)


if __name__ == "__main__":
    unittest.main()

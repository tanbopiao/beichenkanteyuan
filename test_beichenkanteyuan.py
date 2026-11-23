"""北辰勘慝院（BEICHEN-KANTEYUAN）算子单测：名帖完整、行为达标、只增不覆盖。"""
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

    def test_issue_order_levels(self):
        heavy = self.op.issue_order("越权访问", "重")
        self.assertEqual(heavy["status"], "pending_xuangui")
        light = self.op.issue_order("巡检异常", "察")
        self.assertEqual(light["status"], "issued")
        with self.assertRaises(ValueError):
            self.op.issue_order("x", "乱")

    def test_pardon(self):
        order = self.op.issue_order("越权访问", "重")
        pardoned = self.op.pardon(order["order_id"])
        self.assertEqual(pardoned["status"], "pardoned")
        with self.assertRaises(KeyError):
            self.op.pardon("BK-9999")
        with self.assertRaises(ValueError):
            self.op.pardon(order["order_id"])


if __name__ == "__main__":
    unittest.main()

"""北辰勘慝院（BEICHEN-KANTEYUAN）算子测试套件：名帖完整、三令分权行为达标、台账防篡改、v1 行为回归重放。

覆盖：勘官发令（issue_order）、玄圭允行（approve）、勘慝执行（execute）、
赦令（pardon）、台账（ledger/seal/verify_ledger 前缀快照哈希防篡改）、只增不覆盖边界。
"""

import unittest

from beichenkanteyuan import BeichenKanteyuan


class TestMingtie(unittest.TestCase):
    """名帖与道统映射一致性。"""

    def setUp(self):
        self.op = BeichenKanteyuan()

    def test_describe_repo(self):
        self.assertEqual(self.op.describe()["repo"], "beichenkanteyuan")

    def test_describe_cn(self):
        self.assertEqual(self.op.describe()["cn"], "北辰勘慝院")

    def test_describe_code(self):
        self.assertEqual(self.op.describe()["code"], "BEICHEN-KANTEYUAN")

    def test_describe_duty(self):
        self.assertIn("三令分权", self.op.describe()["duty"])

    def test_describe_mingwen(self):
        self.assertTrue(self.op.describe()["mingwen"])

    def test_describe_anchor(self):
        self.assertTrue(self.op.describe()["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))


class TestKanGuan(unittest.TestCase):
    """勘官：按令级发令，重令候允、察令即发。"""

    def setUp(self):
        self.op = BeichenKanteyuan()

    def test_issue_zhong_pending(self):
        order = self.op.issue_order("慝甲", "重")
        self.assertEqual(order["status"], "pending_xuangui")

    def test_issue_cha_issued(self):
        order = self.op.issue_order("慝乙", "察")
        self.assertEqual(order["status"], "issued")

    def test_issue_invalid_level(self):
        with self.assertRaises(ValueError):
            self.op.issue_order("慝丙", "大")

    def test_issue_order_ids_sequential(self):
        first = self.op.issue_order("慝甲", "察")["order_id"]
        second = self.op.issue_order("慝乙", "察")["order_id"]
        self.assertNotEqual(first, second)

    def test_issue_records_event(self):
        self.op.issue_order("慝甲", "察")
        self.assertEqual(self.op.ledger()[-1]["event"], "issue_order")


class TestYunXing(unittest.TestCase):
    """玄圭允行：重令得允乃行。"""

    def setUp(self):
        self.op = BeichenKanteyuan()

    def test_approve_pending_order(self):
        order = self.op.issue_order("慝甲", "重")
        self.assertEqual(self.op.approve(order["order_id"])["status"], "issued")

    def test_approve_cha_order_rejected(self):
        order = self.op.issue_order("慝乙", "察")
        with self.assertRaises(ValueError):
            self.op.approve(order["order_id"])

    def test_approve_pardoned_rejected(self):
        order = self.op.issue_order("慝甲", "重")
        self.op.pardon(order["order_id"])
        with self.assertRaises(ValueError):
            self.op.approve(order["order_id"])

    def test_approve_nonexistent(self):
        with self.assertRaises(KeyError):
            self.op.approve("BK-9999")


class TestZhiCai(unittest.TestCase):
    """勘慝乃行：已允之令执行处置。"""

    def setUp(self):
        self.op = BeichenKanteyuan()

    def test_execute_issued_order(self):
        order = self.op.issue_order("慝甲", "察")
        self.assertEqual(self.op.execute(order["order_id"])["status"], "executed")

    def test_execute_pending_rejected(self):
        order = self.op.issue_order("慝甲", "重")
        with self.assertRaises(ValueError):
            self.op.execute(order["order_id"])

    def test_execute_after_approve(self):
        order = self.op.issue_order("慝甲", "重")
        self.op.approve(order["order_id"])
        self.assertEqual(self.op.execute(order["order_id"])["status"], "executed")

    def test_execute_twice_rejected(self):
        order = self.op.issue_order("慝甲", "察")
        self.op.execute(order["order_id"])
        with self.assertRaises(ValueError):
            self.op.execute(order["order_id"])

    def test_execute_nonexistent(self):
        with self.assertRaises(KeyError):
            self.op.execute("BK-9999")


class TestSheLing(unittest.TestCase):
    """赦令唯宗伯：未结之令可赦，赦后留档不销。"""

    def setUp(self):
        self.op = BeichenKanteyuan()

    def test_pardon_keeps_record(self):
        order = self.op.issue_order("慝甲", "察")
        pardoned = self.op.pardon(order["order_id"])
        self.assertEqual(pardoned["status"], "pardoned")
        self.assertIn(order["order_id"], self.op.orders)

    def test_double_pardon_rejected(self):
        order = self.op.issue_order("慝甲", "察")
        self.op.pardon(order["order_id"])
        with self.assertRaises(ValueError):
            self.op.pardon(order["order_id"])

    def test_pardon_nonexistent(self):
        with self.assertRaises(KeyError):
            self.op.pardon("BK-9999")

    def test_pardon_records_event(self):
        order = self.op.issue_order("慝甲", "察")
        self.op.pardon(order["order_id"])
        self.assertEqual(self.op.ledger()[-1]["event"], "pardon")


class TestLedgerTamperEvident(unittest.TestCase):
    """台账防篡改：前缀快照哈希，篡改现形，合法增长不算篡改。"""

    def setUp(self):
        self.op = BeichenKanteyuan()

    def test_ledger_returns_copy(self):
        self.op.issue_order("慝甲", "察")
        ledger = self.op.ledger()
        ledger.clear()
        self.assertEqual(len(self.op.ledger()), 1)

    def test_seal_returns_digest(self):
        self.op.issue_order("慝甲", "察")
        digest = self.op.seal()
        self.assertIsInstance(digest, str)
        self.assertEqual(len(digest), 64)

    def test_verify_without_seal_is_true(self):
        self.op.issue_order("慝甲", "察")
        self.assertTrue(self.op.verify_ledger())

    def test_verify_after_legal_growth(self):
        """封存后合法新增（发令、允行、赦令）不算篡改。"""
        self.op.issue_order("慝甲", "察")
        self.op.seal()
        self.op.issue_order("慝乙", "重")
        self.op.pardon("BK-0001")
        self.assertTrue(self.op.verify_ledger())

    def test_tamper_past_event_detected(self):
        """封存后篡改历史台账，验封现形。"""
        self.op.issue_order("慝甲", "察")
        self.op.seal()
        self.op.events[0]["event"] = "pardon"  # 模拟篡改历史
        self.assertFalse(self.op.verify_ledger())

    def test_tamper_delete_event_detected(self):
        self.op.issue_order("慝甲", "察")
        self.op.issue_order("慝乙", "重")
        self.op.seal()
        del self.op.events[0]  # 模拟删档
        self.assertFalse(self.op.verify_ledger())

    def test_reseal_after_growth(self):
        """再次封存以新前缀为准。"""
        self.op.issue_order("慝甲", "察")
        self.op.seal()
        self.op.issue_order("慝乙", "察")
        self.op.seal()
        self.op.events[0]["event"] = "pardon"
        self.assertFalse(self.op.verify_ledger())

    def test_verify_with_expect_full_hash(self):
        self.op.issue_order("慝甲", "察")
        digest = self.op.seal()
        self.assertTrue(self.op.verify_ledger(expect=digest))
        self.op.issue_order("慝乙", "察")
        self.assertFalse(self.op.verify_ledger(expect=digest))


class TestRegressionV1(unittest.TestCase):
    """v1 行为回归重放：原 test_beichenkanteyuan.py 核心行为原样保留。"""

    def test_v1_issue_levels_regression(self):
        op = BeichenKanteyuan()
        self.assertEqual(op.issue_order("慝甲", "重")["status"], "pending_xuangui")
        self.assertEqual(op.issue_order("慝乙", "察")["status"], "issued")
        with self.assertRaises(ValueError):
            op.issue_order("慝丙", "大")

    def test_v1_pardon_regression(self):
        op = BeichenKanteyuan()
        order = op.issue_order("慝甲", "察")
        self.assertEqual(op.pardon(order["order_id"])["status"], "pardoned")
        with self.assertRaises(ValueError):
            op.pardon(order["order_id"])
        with self.assertRaises(KeyError):
            op.pardon("BK-0000")

    def test_only_grows_no_removal(self):
        """只增不覆盖：v0.1 保留 v1 全部公开方法。"""
        for method in ("describe", "issue_order", "pardon", "approve",
                       "execute", "ledger", "seal", "verify_ledger"):
            self.assertTrue(callable(getattr(BeichenKanteyuan, method, None)), method)


if __name__ == "__main__":
    unittest.main()

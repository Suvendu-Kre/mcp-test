import unittest
from agents.main_agent import Agent

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent()

    def test_agent_response(self):
        response = self.agent.run("What is 2 + 2?")
        self.assertIn("4", response)

    def test_agent_calculate_tool(self):
        response = self.agent.run("Calculate 5 * 5")
        self.assertIn("25", response)

if __name__ == '__main__':
    unittest.main()
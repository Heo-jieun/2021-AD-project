import unittest
from gameLogic import *

class testGameLogic(unittest.TestCase):

    def setUp(self):
        self.decisionTree = decisionTreeOperation()
        self.dataset = [[0,1,0,0],[0,1,0,1],[1,0,0,0],[1,0,1,0],[1,0,1,1],[0,0,0,0],[0,0,1,0],[1,0,1,0]]
        self.result = [0,0,1,1,0,0,1,1]

    def test_gini(self):
        self.assertEqual(self.decisionTree.gini(self.result),0.5)

    def test_findBestSplit(self):
        best_gain, self.best_question = self.decisionTree.findBestSplit(self.dataset, self.result)
        if best_gain > 0 :
            oper_check = True

        self.assertTrue(oper_check, True)

    def test_information_gain(self):
        self.info_gain = self.decisionTree.information_gain(self.result, self.label_subsets)
        if self.info_gain > 0.5 :
            info_gain_value = True
        self.assertTrue(info_gain_value, True)

    def test_split(self):
        data_subsets, self.result_subsets = self.decisionTree.split(self.dataset, self.result, self.best_question, 1)
        if len(data_subsets) < self.dataset:
            dataSmaller_check = True
        if len(self.result_subsets) < self.result :
            resultSmaller_check = True
        self.assertTrue(dataSmaller_check, True)
        self.assertTrue(resultSmaller_check, True)

    def test_bestSplit(self):
        self.data_subsets, self.label_subsets = self.decisionTree.bestSplit(self.dataset, self.result, 0)
        if len(self.data_subsets) < len(self.dataset):
            dataSmaller_check = True
        if len(self.label_subsets) < len(self.result):
            labelSmaller_check =True
        self.assertTrue(dataSmaller_check, True)
        self.assertTrue(labelSmaller_check, True)


if __name__ == '__main__':
    unittest.main()

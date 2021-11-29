from collections import Counter

class decisionTreeOperation:
    # gini impurity를 계산 하는 함수
    def gini(self, dataset):
        impurity = 1
        label_counts = Counter(dataset)
        for label in label_counts:
            prob_label = label_counts[label] / len(dataset)
            impurity -= prob_label ** 2
        return impurity

    # 정보이득 계산하는 함수
    def information_gain(self, previous_labels, split_labels):
        info_gain = self.gini(previous_labels)

        for subset in split_labels:
            info_gain -= self.gini(subset) * len(subset)/len(previous_labels)

        return info_gain

    # 사용자의 질문에 맞추어 데이터를 걸러내는 split
    def split(self, dataset, data_result, feat_question, user_answer):
        data_subsets = []
        result_subsets = []

        for i in range(len(dataset)):
            if(dataset[i][feat_question] == user_answer):
                data_subsets.append(dataset[i])
                result_subsets.append((data_result[i]))

        return data_subsets, result_subsets

    # 최적의 질문을 찾기위해 gini를 계산 할 때 호줄 되는 split
    def bestSplit(self, dataset, data_result, feat_question ):
        data_subsets = []
        label_subsets = []

        counts = list(set([data[feat_question] for data in dataset]))
        counts.sort()

        for k in counts:
            split_data_subsets = []
            split_label_subsets = []
            for i in range(len(dataset)):
                if(dataset[i][feat_question] == k):
                    split_data_subsets.append(dataset[i])
                    split_label_subsets.append(data_result[i])
            data_subsets.append(split_data_subsets)
            label_subsets.append(split_label_subsets)
        return data_subsets, label_subsets

    # 모든 질문의 정보 이득을 계산해서 최적의 질문을 찾는 함수
    def findBestSplit(self, dataset, result_data):
        best_gain = 0
        best_question = 0

        for question in range(len(dataset[0])):
            data_subsets, label_subsets = self.bestSplit(dataset, result_data, question)
            gain = self.information_gain(result_data, label_subsets)
            if gain > best_gain :
                best_gain, best_question = gain, question
        return best_gain, best_question

if __name__ == '__main__':
    import questionData

    game = decisionTreeOperation()

    data_subsets = questionData.dataset
    result_subsets = questionData.data_result

    best_gain = 1

    while best_gain != 0:
        best_gain, best_question = game.findBestSplit(data_subsets, result_subsets)

        print(questionData.questions[best_question])
        user_answer = int(input("0(NO) or 1(Yes) : "))

        data_subsets, result_subsets = game.split(data_subsets, result_subsets, best_question, user_answer)

    answer = questionData.people_name[list(Counter(result_subsets))[0]]
    print(answer)
    questionData.dataset = questionData.dataset.append([0,0,0,0,])

# Data for guessing

# data file 처리
def dataFile(fileName, type) :
    dataArray = []
    fDataArray = open(fileName, "r")

    while True:
        line = fDataArray.readline()
        if not line:
            break

        line_strip = line.rstrip('\n')
        line_split = line_strip.split(',')
        if type == "dataset":
            dataArray.append(line_split)
        elif type == "data_result":
            dataArray += line_split
    fDataArray.close()
    dataArray = [list(map(int, dataArray[idx])) for idx in range(len(dataArray))] if type == "dataset" else list(map(int,dataArray))
    return dataArray

dataset = dataFile(".\gameData\guessData", "dataset")
data_result = dataFile(".\gameData\guessResult", "data_result")

# question array
questions = ['파워플한 안무를 좋아한다.',
             '위트있고 센스있는 안무가 좋다.',
             '좋은 리더보다는 팀을 위한 리더이다.',
             '힙합을 좋아한다.',
             '빨간색이 생각난다.',
             '꿈을 이루기 위해서라면 뭐든 할 것 같다.',
             '이름이 본명과 관련되어 있다.',
             'k-pop 안무를 많이 만든 댄서다.',
             'YG와 관련있다.',
             '춤을 가르치는 교수님이다.',
             '평소 진한 화장을 좋아하는 댄서다.',
             '스우파 전부터 원래 유명한 댄서이다.',
             '별명이 "아기고양이" 이다.'
             ]

# people_name array
people_name= ["아이키", "효진초이", "리정", "가비",
                "모니카", "노제", "리헤이", "허니제이"]

if __name__ == '__main__':

    print(len(questions) ==len(dataset[0]))
    print(len(dataset) == len(data_result))

    print(dataset)
    print(data_result)
    print(questions )
    print(people_name)
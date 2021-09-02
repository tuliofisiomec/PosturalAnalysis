from imageai.Classification.Custom import CustomImageClassification


if __name__ == '__main__':
    prediction = CustomImageClassification()
    prediction.setModelTypeAsResNet50()
    prediction.setModelPath('posture/models/model_ex-001_acc-1.000000.h5')
    prediction.setJsonPath('posture/json/model_class.json')
    prediction.loadModel(num_objects=1)

    predictions, probabilies = prediction.predictImage('testimage2.png', result_count=1)

    for pred, prob in zip(predictions, probabilies):
        print(pred, " : ", prob)
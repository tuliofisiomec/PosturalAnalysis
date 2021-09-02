from imageai.Classification.Custom import CustomImageClassification


if __name__ == '__main__':
    prediction = CustomImageClassification()
    prediction.setModelTypeAsResNet50()
    prediction.setModelPath('PostureModel/models/model_ex-004_acc-0.828571.h5')
    prediction.setJsonPath('PostureModel/json/model_class.json')
    prediction.loadModel(num_objects=2)

    predictions, probabilies = prediction.predictImage('TestingImages/cat.png', result_count=2)

    for pred, prob in zip(predictions, probabilies):
        print(pred, " : ", prob)
from imageai.Classification.Custom import ClassificationModelTrainer


if __name__ == '__main__':

    model_trainer = ClassificationModelTrainer()
    model_trainer.setModelTypeAsResNet50()
    model_trainer.setDataDirectory('PostureModel')
    model_trainer.trainModel(
        num_objects=2, 
        num_experiments=10, 
        batch_size=32,
        show_network_summary=True
    )

import yaml
import preprocess as pre  # type: ignore
from train_classifier import main  # type: ignore

with open("./config.yaml") as f:
    conf = yaml.safe_load(f)


def eval_face(input_dir):
    """
    function that recognizes the face on a picture.
    input: location of the picture. (str)
    output: predicted label of the picture. (str)
    errors:
    + picture_name does not exist/is not and image - throw type error
    + no positive match to any of the labels - throw nonexistent error
    """

    # se procesa la foto.
    pre.main(input_dir, input_dir, 180)

    # se evalúa la foto con el modelo.
    return main(
        input_dir,
        conf["model_path"],
        conf["classifier_output_path"],
        conf["batch_size"],
        conf["num_threads"],
        conf["num_epochs"],
        conf["min_num_images_per_class"],
        conf["split_ratio"],
        False
    )


def add_face(input_dir):
    """
    function that retrains the model to add a new face.
    input: location of the images. (str)
    output: error code, 0 otherwise. (exception, none)
    errors:
    + pictures_folder is not a folder - throw type error
    + pictures_folder contains a non-image - fail silently and continue
      for the rest
    + pictures_folder does not have [enough] pictures - throw exception and
      exit
    + pictures_folder contains pictures that are not from the same people -
      this kills the model.
    """

    # se procesan las fotos.
    pre.main(input_dir, input_dir, 180)

    # se cargan los embeddings originales, reentrena el modelo, y guarda
    # en el mismo directorio el nuevo modelo y embeddings.
    main(
        input_dir,
        conf["model_path"],
        conf["classifier_output_path"],
        conf["batch_size"],
        conf["num_threads"],
        conf["num_epochs"],
        conf["min_num_images_per_class"],
        conf["split_ratio"],
        True
    )


def new_model(input_dir):
    """
    function that generates a new model from a folder full of pictures.
    """
    pass
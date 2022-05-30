
import numpy as np
from preprocessing import preprocessMed


def creeEq(imgIn2, p1, p2, p3, p4, p5, p6, num_arg):
    rgbImg2 = imgIn2

  # init
    img2Out = np.zeros(np.size(rgbImg2))

    if (num_arg == 2):
        imgInModel = p1
      # use imgInModel
        rMean = np.mean(np.vectorize(imgInModel[:, :, 1]))
        rStd = np.std(np.vectorize(imgInModel[:, :, 1]))
        gMean = np.mean(np.vectorize(imgInModel[:, :, 2]))
        gStd = np.std(np.vectorize(imgInModel[:, :, 2]))
        bMean = np.mean(np.vectorize(imgInModel[:, :, 3]))
        bStd = np.std(np.vectorize(imgInModel[:, :, 3]))

    else:
        rMean = p1
        rStd = p2
        gMean = p3
        gStd = p4
        bMean = p5
        bStd = p6

    img2Out[:, :, 1] = preprocessMed(rgbImg2[:, :, 1], rMean, rStd)
    img2Out[:, :, 2] = preprocessMed(rgbImg2[:, :, 2], gMean, gStd)
    img2Out[:, :, 3] = preprocessMed(rgbImg2[:, :, 3], bMean, bStd)

    # % cast back
    img2Out = np.cast(img2Out, imgIn2)

    return img2Out

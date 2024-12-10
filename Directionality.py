import os
from fiji.analyze.directionality import Directionality_
from ij import IJ, ImagePlus

folder_path = r"C:\Users\szktk\Desktop\Suzuki\data\Experiment\zigzag\DPC"

tiff_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]

for index, tiff_file in enumerate(tiff_files, start=1):
    try:
        tiff_file_path = os.path.join(folder_path, tiff_file)
        print("Processing file {}/{}: {}".format(index, len(tiff_files), tiff_file_path))

        image_plus = IJ.openImage(tiff_file_path)

        dir = Directionality_()

        dir.setImagePlus(image_plus)
        dir.setMethod(Directionality_.AnalysisMethod.FOURIER_COMPONENTS)
        dir.setBinNumber(30)
        dir.setBinStart(-60)
        dir.setBuildOrientationMapFlag(True)

        dir.computeHistograms()
        dir.fitHistograms()

        plot_frame = dir.plotResults()
        plot_frame.setVisible(True)

        data_frame = dir.displayFitAnalysis()
        data_frame.setVisible(True)

        table = dir.displayResultsTable()
        table.show("Directionality histograms for {}".format(tiff_file))

        stack = dir.getOrientationMap()
        ImagePlus("Orientation map for {}".format(tiff_file), stack).show()

        print("Finished processing file {}/{}: {}".format(index, len(tiff_files), tiff_file_path))
    except Exception as e:
        print("Error processing file {}: {}".format(tiff_file, e))
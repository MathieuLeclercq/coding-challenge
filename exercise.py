
import itk
import vtk
import argparse



def GetArguments():  
  parser = argparse.ArgumentParser(description="Read An Image")
  parser.add_argument("inputImage")
  parser.add_argument("outputImage")
  parser.add_argument("radius")
  args = parser.parse_args()
  return args


def ReadImage():
  args = GetArguments()
  print('Reading image: ',args.inputImage)
  pixelType = itk.UC
  imageType = itk.Image[pixelType, 2]
  return imageType 
  

def FilterImage(imageType):
  print("Filtering image...")
  args = GetArguments()

  #Apply filter to the image
  reader = itk.ImageFileReader[imageType].New()
  reader.SetFileName(args.inputImage)
  meanFilter = itk.MeanImageFilter[imageType, imageType].New()
  meanFilter.SetInput(reader.GetOutput())
  meanFilter.SetRadius(int(args.radius))

  # Write the output file
  writer = itk.ImageFileWriter[imageType].New()
  writer.SetFileName(args.outputImage)
  writer.SetInput(meanFilter.GetOutput())
  writer.Update()
  print("Filtered image created: ",args.outputImage)

def DisplayImage(image1,image2):

  # Read the source files.
  reader1 = vtk.vtkPNGReader()
  reader1.SetFileName(image1)
  reader1.Update()

  reader2 = vtk.vtkPNGReader()
  reader2.SetFileName(image2)
  reader2.Update()

  # Display the image
  actor1 = vtk.vtkImageActor()
  actor1.GetMapper().SetInputConnection(reader1.GetOutputPort())

  actor2 = vtk.vtkImageActor()
  actor2.GetMapper().SetInputConnection(reader2.GetOutputPort())  

  renderer1 = vtk.vtkRenderer()
  renderer1.AddActor(actor1)
  renderer1.SetViewport(0.0, 0.0, 0.5, 1.0)

  renderer2 = vtk.vtkRenderer()
  renderer2.AddActor(actor2)
  renderer2.SetViewport(0.5, 0.0, 1.0, 1.0)

  window = vtk.vtkRenderWindow()
  window.AddRenderer(renderer1)
  window.AddRenderer(renderer2)

  # Set up the interaction
  interactor = vtk.vtkRenderWindowInteractor()
  interactor.SetRenderWindow(window)
  window.SetWindowName('Result')
  interactor.Initialize()
  interactor.Start()

def main():
  args = GetArguments()
  image = ReadImage()
  FilterImage(image)
  DisplayImage(args.inputImage,args.outputImage)

if __name__ == '__main__':
  main()

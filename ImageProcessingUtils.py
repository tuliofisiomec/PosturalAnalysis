import cv2
import os


class ImageAugmenter:
    '''
    Pass in target directory to constructor.
    ImageAugmenter.run() will add a flipped and scaled version of every
    photo in given directory.
    '''
    
    def __init__(self, image_directory: str = None):
        self.image_directory = image_directory

    def flip_all_images(self):
        '''
        goes through a directory and adds a flipped version of the image
        '''
        for f in os.listdir(self.image_directory):
            print(f)
            self.flip_image(f)
    
    def flip_image(self, img_file: str):
        try:
            img = cv2.imread(f'{self.image_directory}/{img_file}')
            flipped_img = img[:, ::-1, :]
            cv2.imwrite(f'{self.image_directory}/{img_file[:-5]}_flipped.jpeg', flipped_img)
        except Exception as e:
            print(e)

    def scale_and_crop_all_images(self):
        '''
        goes through a directory and adds a zoomed in version of the image
        '''
        for f in os.listdir(self.image_directory):
            if f.endswith('.jpeg'):
                self.scale_then_crop(f)

    def scale_then_crop(self, img_file: str):
        '''
        scales and image, and crops image
        '''
        scaled_img = self.scale_up_image(img_file)
        self.crop_image(scaled_img, img_file)

    def scale_up_image(self, img_file: str):
        '''
        scales up and image and returns a numpy array of image
        '''
        img = cv2.imread(f'{self.image_directory}/{img_file}')
        new_size = 450
        resized = cv2.resize(img, (new_size, new_size), interpolation=cv2.INTER_LINEAR)
        return resized

    def crop_image(self, img_obj, img_file: str):
        '''
        takes numpy array of image, crops it to 360 X 360, then writes it to folder
        '''
        cropped = img_obj[20:380, 20:380]
        cv2.imwrite(f'{self.image_directory}/{img_file[:-5]}_scaled.jpeg', cropped)

    def run(self):
        self.flip_all_images()
        self.scale_and_crop_all_images()


class ImageSlicer:
    '''
    Pass in target directory to constructor.
    ImageSlicer.run() will slice all photos in a directory in half
    '''

    def __init__(self, image_directory: str = None):
        self.image_directory = image_directory

    def slice_all_images(self):
        '''
        goes through a directory and slices the images in half
        '''
        for f in os.listdir(self.image_directory):
            self.slice_image(f)
    
    def slice_image(self, img_file: str):
        '''
        cuts image in half
        '''
        img = cv2.imread(f'{self.image_directory}/{img_file}')
        if img is not None:
            width = img.shape[1]
            cutoff = width // 2
            s1 = img[:, :cutoff]
            s2 = img[:, cutoff:]
            cv2.imwrite(f'SlicedImages/{img_file[:-5]}_s1.jpeg', s1)
            cv2.imwrite(f'SlicedImages/{img_file[:-5]}_s2.jpeg', s2)

    def run(self):
        self.slice_all_images()


class ImageResizer:
    '''
    Pass in target directory to constructor.
    Pads and resizes all images in a directory to 360 X 360
    '''
    def __init__(self, image_directory: str):
        self.image_directory = image_directory
        self.uniform_size = 360

    def resize_all_images(self):
        for f in os.listdir(self.image_directory):
            self.resize(f)

    def resize(self, image_file: str = None):
        '''
        resizes and adds padding to image
        '''
        img = cv2.imread(f'{self.image_directory}/{image_file}')
        old_size = img.shape[:2]
        ratio = float(self.uniform_size) / max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])
        new_img = cv2.resize(img, (new_size[1], new_size[0]))
        delta_w = self.uniform_size - new_size[1]
        delta_h = self.uniform_size - new_size[0]
        top, bottom = delta_h//2, delta_h - (delta_h//2)
        left, right = delta_w//2, delta_w - (delta_w//2)
        color = [0, 0, 0]
        final_image = cv2.copyMakeBorder(new_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        cv2.imwrite(f'ResizedImages/{image_file[:-5]}.jpeg', final_image)
    
    def run(self):
        self.resize_all_images()

        
if __name__ == '__main__':

    '''
    Uncomment all these if you want to run the whole process from the start.
    '''

    # # First slice all the images in half
    # slicer = ImageSlicer('RoundedShoulderRaw')
    # slicer.run()

    # # Next, pad and resize
    # padder = ImageResizer('SlicedImages')
    # padder.run()

    # # Finally, add flipped and scaled versions of every image
    # augmenter = ImageAugmenter('SelectedImages')
    # augmenter.run()

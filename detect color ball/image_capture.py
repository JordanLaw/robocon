import cv2
import realsense
import basket_location
import zoom_function

basket_location = basket_location.basket_location()

basket = basket_location.basket_location()

class image:
    def __int__(self):
        pass

    def image_capture(self, bg_removed, color_image):

        images_removebg = bg_removed

        imageFrame = images_removebg

        for x in basket:
            cv2.rectangle(imageFrame, (x[2], x[0]), (x[3], x[1]), (0, 255, 0), 2)

        cropped_img_1_1 = imageFrame[basket[0][0]:basket[0][1], basket[0][2]:basket[0][3]]
        cropped_img_1_2 = imageFrame[basket[1][0]:basket[1][1], basket[1][2]:basket[1][3]]
        cropped_img_1_3 = imageFrame[basket[2][0]:basket[2][1], basket[2][2]:basket[2][3]]

        img_1_1 = zoom_function.zoom_at(cropped_img_1_1, 3)
        img_1_2 = zoom_function.zoom_at(cropped_img_1_2, 3)
        img_1_3 = zoom_function.zoom_at(cropped_img_1_3, 3)
        img = [img_1_1, img_1_2, img_1_3]

        return img
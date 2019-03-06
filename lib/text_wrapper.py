class TextWrapper:
    @staticmethod
    def wrap_text_by_width(text, font, max_width):
        """
        Wrap text based on a maximum width
        :param text: text to wrap
        :param font: font used to calculation
        :param max_width: maximum width
        :return: text wrapped
        """
        lines = []

        # If the width of the text is smaller than image width
        # we don't need to split it, just add it to the lines array
        # and return
        if font.getsize(text)[0] <= max_width:
            lines.append(text)
        else:
            # split the line by spaces to get words
            words = text.split(' ')
            i = 0
            # append every word to a line while its width is shorter than image width
            while i < len(words):
                line = ''
                while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                # when the line gets longer than the max width do not append the word,
                # add the line to the lines array
                lines.append(line)

        return lines

    @staticmethod
    def text_size(lines, font, is_in_vertical_mode=False):
        """
        Text wrapped height calculation
        :param lines: lines wrapped from TextWrapper.wrap_text_by_width
        :param font: font size to width calculation
        :return: height in pixel
        """
        height_calculation_status = False
        height = 0
        width = 0

        if lines:
            if isinstance(lines, list):
                for line in lines:
                    if not is_in_vertical_mode:
                        width = font.getsize(line)[0]
                        height += font.getsize(line)[1]
                    else:
                        width = font.getsize(line)[1]
                        height += font.getsize(line)[0]
            else:
                if not is_in_vertical_mode:
                    width = font.getsize(lines)[0]
                    height = font.getsize(lines)[1]
                else:
                    width = font.getsize(lines)[1]
                    height = font.getsize(lines)[0]
            height_calculation_status = True

        return height_calculation_status, (width, height)

    @staticmethod
    def points_to_pixel(points):
        """
        Convert points value to pixel value
        :param points: points value
        :return: pixel value
        """
        return int(points / 0.75)

    @staticmethod
    def pixel_to_points(pixel):
        """
        Convert pixel value to points value
        :param pixel: pixel value
        :return: points value
        """
        return int(pixel * 0.75)

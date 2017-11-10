clear all;
close all;

img = imread('tux.jpg');
img = rgb2gray(img);
imshow(img);
title('original image');

img_gaussian = imnoise(img,'gaussian',0,0.01);
img_impulse = imnoise(img, 'salt & pepper', 0.01);
subplot(2,2,1);
imshow(img_gaussian);
title('image with gaussian noise');
subplot(2,2,3);
imshow(img_impulse);
title('image with impulse noise');

img_gaussian_nl = img_gaussian;
img_impulse_nl = img_impulse;

for i=1:size(img,1)
    for j = 1:size(img,2)
        w_gauss=0;
        w_impulse=0;
        weight=0;
        for k = 1:size(img,1)
            for l = 1:size(img,2)
                dist = sqrt((i-k)^2 + (j-l)^2);
                temp = exp(-dist * dist / 6);
                w_gauss = w_gauss + temp * double(img_gaussian(k,l));
                w_impulse = w_impulse + temp * double(img_impulse(k,l));
                weight = weight + temp;
            end
        end
        img_gaussian_nl(i,j) = w_gauss/weight;   
        img_impulse_nl(i, j) = w_impulse/weight;
    end
end

subplot(2,2,2);
imshow(img_gaussian_nl);
title('filtered image');
subplot(2,2,4);
imshow(img_impulse_nl);
title('filtered image');
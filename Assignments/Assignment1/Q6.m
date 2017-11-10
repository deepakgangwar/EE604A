clear all;
close all;
img = imread('lena.jpg');
subplot(2,3,1);
imshow(img);
title('Original Image');

fft_img = fft2(img);
fft_abs = abs(fft_img);
fft_phase = angle(fft_img);

subplot(2,3,2);
imshow(mat2gray(log(abs(fftshift(fft_img)))));
title('Log of Absolute of fft');

subplot(2,3,3)
imshow(mat2gray(fft_phase));
title('Phase of fft');

subplot(2,3,4)
imshow(uint8(ifftshift(ifft2(fft_abs))),[]);
title('Reconstruction Using Magnitude');

subplot(2,3,6)
imshow((ifft2(exp(1i*fft_phase))),[]);
title('Reconstruction Using Phase');
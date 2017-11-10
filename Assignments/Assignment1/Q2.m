clear all;
close all;

% ref = imread('uniform.jpg');
target = imread('lena.jpg');
ref = imread('baboon.png');

ref_hist = imhist(ref);
target_hist = imhist(target);

cdf_ref = cumsum(ref_hist);
cdf_target = cumsum(target_hist);

Mapping = zeros(1,size(ref_hist,1));

for idx = 1 : size(ref_hist,1)
    [~,index] = min(abs(cdf_target(idx) - cdf_ref));
    Mapping(idx) = index-1;
end

matched = uint8(Mapping(target+1));
subplot(2,3,1);
imshow(ref);
title('ref image');

subplot(2,3,2);
imshow(target);
title('Target image');

subplot(2,3,3);
imshow(matched);
title('Matched image');

subplot(2,3,4);
imhist(ref);

subplot(2,3,5);
imhist(target);

subplot(2,3,6);
imhist(matched);
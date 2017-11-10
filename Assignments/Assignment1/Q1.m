clear all;
close all;
iterations = 100;
X = randn(1,100);
min = min(X);
max = max(X);
levels = 4;
interval=zeros(1,levels+1);
for i=1:levels+1
    interval(i)=min+(i-1)*(max-min)/levels;
end
number=zeros(1,levels);
summation=zeros(1,levels);
for i=1:iterations
    for k=1:levels
        for j=1:length(X)
            if(X(j)<interval(k+1) && X(j)>=interval(k))
                number(k)=number(k)+1;
                summation(k)=summation(k)+X(j);
            end
        end
        if number(k)==0
        summation(k)=(interval(k)+interval(k+1))/2;
        number(k)=1;
        end
        mean(k)=summation(k)/number(k);
        if k~=1
            interval(k)=(mean(k-1)+mean(k))/2;
        end
    end
    for j=1:levels
        for t=1:length(X)
            if(X(t)<interval(j+1) && X(t)>=interval(j))
                quant_X(t)=mean(j);
            end
        end
    end
    MSE(i)=sum((X-quant_X).^2)/length(X);
end
disp('Transition Levels: ')
disp(interval)
disp('Representation Levels: ')
disp(mean)

figure, plot(MSE)
xlabel('No. of iterations');
ylabel('Mean Squared Error');
title('MSE vs no of iterations');
text(iterations,MSE(iterations),['(' num2str(MSE(iterations)) ')']);
hold on
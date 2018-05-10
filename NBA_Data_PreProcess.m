% Test Case For TopK Streaming using Angular Hashing method

% p1 = [-0.5, -0.5];
% p2 = [-0.5, 0.5];
% p3 = [0.5, -0.5];
% p4 = [0.5, 0.5];
% p5 = [-0.1, -0.1];
% 
% p = [p1, p2, p3, p4, p5];
% figure
% plot(p, '*')
% plot(x,y,'*')

x = [-0.5, -0.5, 0.5, 0.5, -0.1];
y = [-0.5, 0.5, -0.5, 0.5, -0.1];
figure
plot(x, y, '*')
grid on
axis([-2 2 -2 2])

xq1 = [-1];
yq1 = [-1];

xq2 = [-0.5];
yq2 = [-1];




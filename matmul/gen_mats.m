function gen_mats(side)

	if nargin < 1;

		side = 5; % cube side length

	end

	mn = 1;
	mx = 9;

	a_filename = 'a.txt';
	b_filename = 'b.txt';
	c_filename = 'c.txt';

	a = randi([mn mx], side, side);
	b = randi([mn mx], side, side);
	c = a * b;

	dlmwrite(a_filename, a, ', ');
	dlmwrite(b_filename, b, ', ');
	dlmwrite(c_filename, c, ', ');

end

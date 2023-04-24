#include <bits/stdc++.h>
using namespace std;
int a, b, c, d, e, f;
int N, M, K;
int **s, **g, **h, **p, **q;
int *t;
int max_score = 0;
int **student_solution, **teacher_solution;
void print_solution();
void update_h(int val, int idx);
void update_p(int val, int idx);
void restore_h(int val, int idx);
void restore_p(int val, int idx);
void copy2DArray(int **sourceArray, int **destArray, int rows, int cols);
int **allocate2D(int rows, int cols);
void update_solution();
int calc_score();
bool check(int N);
void input();
void free_arr();
void Try(int n)
// Try to fill p and h 2D matrix to optimize the target function, only check for constraints when the matrixes are fully populated;
{
	for (int i = 0; i < K; i++)
	{
		// Assign students to councils
		if (n < N)
		{
			if (check(n))
			{
				update_h(n, i);
				Try(n + 1);
				restore_h(n, i);
			}
		}
		else
		{
			// Assign teachers to councils
			if (check(n))
			{
				if (n == N + M)
				{
					if (calc_score() > max_score)
					{
						max_score = calc_score();
						update_solution();
					}
				}
				else
				{
					update_p(n - N, i);
					Try(n + 1);
					restore_p(n - N, i);
				}
			}
		}
	}
}
int main()
{
	input();
	Try(0);
	print_solution();
	free_arr();
}

void print_solution()
{
	cout << N << endl;
	for (int i = 0; i < N; i++)
		for (int k = 0; k < K; k++)
			if (student_solution[i][k] == 1)
				cout << k + 1 << " ";
	cout << endl;
	cout << M << endl;
	for (int i = 0; i < M; i++)
		for (int k = 0; k < K; k++)
			if (teacher_solution[i][k] == 1)
				cout << k + 1 << " ";
	cout << endl;
}

void update_p(int val, int idx)
{
	p[val][idx] = 1;
}
void update_h(int val, int idx)
{
	h[val][idx] = 1;
}
void restore_p(int val, int idx)
{
	p[val][idx] = 0;
}
void restore_h(int val, int idx)
{
	h[val][idx] = 0;
}
int calc_score()
{
	int sum = 0;
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < M; j++)
		{
			for (int k = 0; k < K; k++)
			{
				sum += g[i][j] * h[i][k] * p[j][k];
			}
		}
		for (int n = i; n < N; n++)
		{
			for (int k = 0; k < K; k++)
			{
				sum += s[i][n] * h[i][k] * h[n][k];
			}
		}
	}
	return sum;
}
bool check(int n)
{
	for (int i = 0; i < N; i++)
	{
		int teacher_count = 0;
		for (int j = 0; j < M; j++)
		{
			teacher_count += q[i][j];
		}
		if (teacher_count > 1)
		{
			// cout << "More than 1 teacher instruct 1 thesis" << endl;
			return false;
		};
	}
	for (int j = 0; j < M; j++)
	{
		int teacher_count = 0;
		for (int k = 0; k < K; k++)
		{
			teacher_count += p[j][k];
		}
		if (teacher_count > 1)
		{
			// cout << "Teacher is in more than 1 council!";
			return false;
		}
	}
	for (int i = 0; i < N; i++)
	{
		int thesis_count = 0;
		for (int k = 0; k < K; k++)
		{
			thesis_count += h[i][k];
		}
		if (thesis_count > 1)
		{
			// cout << "Thesis is in more than 1 council";
			return false;
		}
	}
	// Only check for other conditions when all students and teachers are assigned value
	if (n == N + M)
	{
		for (int k = 0; k < K; k++)
		{
			int thesis_count = 0;
			int teacher_count = 0;
			for (int i = 0; i < N; i++)
			{
				thesis_count += h[i][k];
			}
			for (int j = 0; j < M; j++)
			{
				teacher_count += p[j][k];
			}
			if (thesis_count > b || thesis_count < a)
			{
				// cout << "Thesis count not in range" << endl;
				return false;
			}
			if (teacher_count > d || teacher_count < c)
			{
				// cout << "Teacher in a council is not in range" << endl;
				return false;
			}
		}
		for (int i = 0; i < N; i++)
		{
			for (int k = 0; k < K; k++)
			{
				if (h[i][k] * p[t[i] - 1][k] != 0)
				{
					// cout << "Teacher should not be in the same council as the thesis" << endl;
					return false;
				}
			}
		}
		for (int i = 0; i < N; i++)
		{
			for (int j = 0; j < M; j++)
			{
				for (int k = 0; k < K; k++)
				{
					if (s[i][j] < e * h[i][k] * h[j][k] && i != j)
					{
						// cout << "Similarity of thesis in a council is not enough!" << endl;
						return false;
					}
					if (g[i][j] < f * p[j][k] * h[i][k])
					{
						// cout << "Similarity of thesis and teacher in a council is not enough!" << endl;
						return false;
					}
				}
			}
		}
	}
	// cout << "Pass all constraints!!!" << N << endl;
	return true;
}
void update_solution()
{
	copy2DArray(p, teacher_solution, M, K);
	copy2DArray(h, student_solution, N, K);
}
void input()
{
	std::fstream myfile("input.txt", ios_base::in);

	myfile >> N >> M >> K;
	myfile >> a >> b >> c >> d >> e >> f;
	s = allocate2D(N, N);
	g = allocate2D(N, M);
	t = new int[N];
	q = allocate2D(N, M);
	p = allocate2D(M, K);
	h = allocate2D(N, K);
	student_solution = allocate2D(N, K);
	teacher_solution = allocate2D(M, K);
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
		{
			myfile >> s[i][j];
		}
	}
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < M; j++)
		{
			myfile >> g[i][j];
		}
	}
	for (int i = 0; i < N; i++)
	{
		myfile >> t[i];
	}
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < M; j++)
		{
			q[i][j] = 0;
		}
		for (int z = 0; z < K; z++)
		{
			h[i][z] = 0;
		}
	}
	for (int i = 0; i < M; i++)
	{
		for (int j = 0; j < K; j++)
		{
			p[i][j] = 0;
		}
	}
	for (int i = 0; i < N; i++)
	{
		q[i][t[i] - 1] = 1;
	}
}
void free_arr()
{
	for (int i = 0; i < N; i++)
	{
		delete[] s[i];
		delete[] g[i];
		delete[] q[i];
		delete[] h[i];
	}
	delete[] s;
	delete[] g;
	delete[] q;
	delete[] h;
	for (int i = 0; i < M; i++)
	{
		delete[] p[i];
	}
	delete[] p;
	delete[] t;
}
void copy2DArray(int **sourceArray, int **destArray, int rows, int cols)
{

	for (int i = 0; i < rows; i++)
	{
		for (int j = 0; j < cols; j++)
		{
			destArray[i][j] = sourceArray[i][j];
		}
	}
}
int **allocate2D(int rows, int cols)
{
	int **arr = new int *[rows];
	for (int i = 0; i < rows; i++)
	{
		arr[i] = new int[cols];
	}
	return arr;
}
#include <bits/stdc++.h>
using namespace std;
int a, b, c, d, e, f;
int n, m, k;
int **s, **g, **h, **p, **q;
int *t;
void print_solution();
void update_h(int nn, int idx);
void update_p(int nn, int idx);
void restore_h(int nn, int idx);
void restore_p(int nn, int idx);
int calc();
bool check(int N);
void input();
void free_arr();
void Try(int N)
// Try to fill p and h 2D matrix to optimize the target function, only check for constraints when the matrixes are fully populated;
{
	for (int i = 0; i < k; i++)
	{
		// Assign students to councils
		if (N < n)
		{
			if (check(N))
			{
				update_h(N, i);
				Try(N + 1);
				restore_h(N, i);
			}
		}
		else
		{
			// Assign teachers to councils
			if (check(N))
			{
				if (N == n + m)
				{
					print_solution();
					cout << "value  is: " << calc() << endl;
				}
				else
				{
					update_p(N - n, i);
					Try(N + 1);
					restore_p(N - n, i);
				}
			}
		}
	}
}
int main()
{
	input();
	Try(0);
	free_arr();
}

void print_solution()
{
	cout << n << endl;
	for (int i = 0; i < n; i++)
		for (int j = 0; j < k; j++)
			if (h[i][j] == 1)
				cout << j + 1 << " ";
	cout << endl;
	cout << m << endl;
	for (int i = 0; i < m; i++)
		for (int j = 0; j < k; j++)
			if (p[i][j] == 1)
				cout << j + 1 << " ";
	cout << endl;
}

void update_p(int nn, int idx)
{
	p[nn][idx] = 1;
}
void update_h(int nn, int idx)
{
	h[nn][idx] = 1;
}
void restore_p(int nn, int idx)
{
	p[nn][idx] = 0;
}
void restore_h(int nn, int idx)
{
	h[nn][idx] = 0;
}
int calc()
{
	int sum = 0;
	for (int i = 0; i < n; i++)
	{
		for (int j = 0; j < m; j++)
		{
			for (int z = 0; z < k; z++)
			{
				sum += g[i][j] * h[i][z] * p[j][z];
			}
		}
		for (int l = 0; l < n; l++)
		{
			for (int k1 = 0; k1 < k; k1++)
			{
				sum += s[i][l] * h[i][k1] * h[l][k1];
			}
		}
	}
	return sum;
}
bool check(int N)
{
	for (int i = 0; i < n; i++)
	{
		int teacher_count = 0;
		for (int j = k; j < m; j++)
		{
			teacher_count += q[i][j];
		}
		if (teacher_count > 1)
		{
			// cout << "More than 1 teacher instruct 1 thesis" << endl;
			return false;
		};
	}
	// Only check for other conditions when all students and teachers are assigned
	if (N == n + m)
	{
		for (int i = 0; i < k; i++)
		{
			int thesis_count = 0;
			int teacher_count = 0;
			for (int j = 0; j < n; j++)
			{
				thesis_count += h[j][i];
			}
			for (int z = 0; z < m; z++)
			{
				teacher_count += p[z][i];
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
		for (int i = 0; i < n; i++)
		{
			for (int j = 0; j < k; j++)
			{
				if (h[i][j] + p[t[i] - 1][j] > 1)
				{
					// cout << "Teacher should not be in the same council as the thesis" << endl;
					return false;
				}
			}
		}
		for (int i = 0; i < n; i++)
		{
			for (int j = 0; j < m; j++)
			{
				for (int z = 0; z < k; z++)
				{
					if (s[i][j] < e * h[i][z] * h[j][z] && i != j)
					{
						// cout << "Similarity of thesis in a council is not enough!" << endl;
						return false;
					}
					if (g[i][j] < f * p[j][z] * h[i][z])
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
void input()
{
	std::fstream myfile("input.txt", ios_base::in);

	myfile >> n >> m >> k;
	myfile >> a >> b >> c >> d >> e >> f;
	s = new int *[n];
	for (int i = 0; i < n; i++)
	{
		s[i] = new int[n];
		for (int j = 0; j < n; j++)
		{
			myfile >> s[i][j];
		}
	}
	g = new int *[n];
	for (int i = 0; i < n; i++)
	{
		g[i] = new int[m];
		for (int j = 0; j < m; j++)
		{
			myfile >> g[i][j];
		}
	}
	t = new int[n];
	for (int i = 0; i < n; i++)
	{
		myfile >> t[i];
	}

	q = new int *[n];
	p = new int *[m];
	h = new int *[n];
	for (int i = 0; i < n; i++)
	{
		q[i] = new int[m];
		h[i] = new int[k];
		for (int j = 0; j < m; j++)
		{
			q[i][j] = 0;
		}
		for (int z = 0; z < k; z++)
		{
			h[i][z] = 0;
		}
	}
	for (int i = 0; i < m; i++)
	{
		p[i] = new int[k];
		for (int j = 0; j < k; j++)
		{
			p[i][j] = 0;
		}
	}
	for (int i = 0; i < n; i++)
	{
		q[i][t[i] - 1] = 1;
	}
}
void free_arr()
{
	for (int i = 0; i < n; i++)
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
	for (int i = 0; i < m; i++)
	{
		delete[] p[i];
	}
	delete[] p;
	delete[] t;
}
#include<stdio.h>
#include<stdlib.h>

#define N 100 // dimension of the matrix (area)
#define DS 100 // number of different sizes of the trees. 



typedef struct{
	unsigned char life: // 0 if there's no tree, 1 if there is 
	unsigned int age; // age of the tree
	unsigned float size; // size of the tree, from 0 to 1. It is normalize with the max size of the trees in the region. 
	char* species; // to know what kind of individual properties will have 


}tree;// every position of the matrix will be a tree, despite there would be any tree. It is a general parameter. It defines what is an individual.



typedef struct{
	unsigned float g_rate; //growth rate
	unsigned float ...
	.
	.
	.

}species; // it is a specific variable. In fact, we can consider it as a template of a tree.


void kill_tree(tree tree)
{
	tree.life=0;
	tree.age=0;
	tree.size=0;
	tree.species="soil";


}// function to kill a tree in a certaian position. It sets its properties to 0

void create_tree(tree tree, char * species, float sizet)
{ 
	tree.life=1;
	tree.age=0;
	tree.size=sizet;
	tree.species=species;
}// fuction to modify the properties of a tree

void random_initiallization (tree forest){



}

void initiallization (tree **forest){

	unsigned i, j;
	for (i=0;i<N;i++)
		for(j=0;j<N;j++)
			{
				forest[j][i]->life=0;
				forest[j][i]->age=0;
				forest[j][i]->size=0;
				forest[j][i]->species="soil";
			}
}//set the initial parameters of the forest to 0

species *new_species (parameters of the variable){

	species * new = malloc(sizeof(species));


	return new;

} // to create tree species. It returns a pointer to species type variable created 

/************+statistical functions********************/
void total_size_distribution (int *v, tree tree)
{
	int i,j;
	for (i=0;i<N;i++)
		for (j=0;j<N;j++)
			v[(tree[j][i].size)*100];
}// sets to every positions of vector V the number of times that a size appears. The n-position represents the frequency of the size n/DS. it's blind to its species





/******************************************************/

int main() {

// ***********************Variable declaration**************************

	int *size_sums; // vector with the size frequency of a given iteration
	tree **forest;
	int i,j;
	int n;

//************************************************************

//******************Variable initiallization***************
	size_sums=malloc(sizeof(DS+1));
	for (i=0;i<DS+1;i++)
		v[i]=0;

	forest=malloc(sizeof(tree)*n);
	for (i=0;i<n;i++)
		forest[i]=malloc(sizeof(tree)*n);
		


	initiallization(forest);


//************************************************************


//********************Main programm****************************
//************************************************************

//*********************External file writting***************************
	
//************************************************************	

return 0;
}
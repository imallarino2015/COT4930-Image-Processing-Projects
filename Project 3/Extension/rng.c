#include<Python.h>

//rotates the bits of the given value by the specified number of shifts
unsigned long long rotateRight(unsigned long long val,int shift){
    shift%=sizeof(val)*8;   //limits the shift size to between 0 and the number of bits-1
    return (val>>shift)|(val<<(sizeof(val)*8-shift));
}

//generates a hash from an array of integers
static PyObject* hash(PyObject* self, PyObject* args){
    unsigned long long result=0;
    
    PyObject* list;
    if(!PyArg_ParseTuple(args,"O",&list)){
        return NULL;
    }
    
    //iterate through the python list
    Py_ssize_t len=PySequence_Length(list);
    for(Py_ssize_t a=0;a<len;a++){
        PyObject* item=PySequence_GetItem(list,a);
        long val=PyLong_AsLong(item);
        result*=rotateRight(val,(a*7)%(sizeof(result)*8));
        result+=86028121;
        result^=rotateRight(result,(val*11)%(sizeof(result)*8));
        Py_DECREF(item);
    }

    return PyLong_FromUnsignedLongLong(result);
}

//random number generator
static PyObject* rndUInt(PyObject* self,PyObject* args){
    static unsigned long long rand=0;
    
    unsigned long long* seed=0;
    if(!PyArg_ParseTuple(args,"|K",&seed)){
        return NULL;
    }
    
    if(seed){
        rand=seed;
    }else{
        rand^=rotateRight(rand,5);
        rand+=0xCCCC;
    }
    
    return PyLong_FromLong(rand);
}

//identify the methods usable by python
static PyMethodDef rng_methods[]={
    {"hash",hash,METH_VARARGS,"Hashes an array of values into a single number"},
    {"rndUInt",rndUInt,METH_VARARGS,"Generates a random integer"},
    {NULL,NULL,0,NULL}
};

//define the module
static struct PyModuleDef rng_definition={
    PyModuleDef_HEAD_INIT,
    "rng",
    "Module for random number generation",
    -1,
    rng_methods
};

//initialize the module
PyMODINIT_FUNC PyInit_rng(void){
    Py_Initialize();
    return PyModule_Create(&rng_definition);
};

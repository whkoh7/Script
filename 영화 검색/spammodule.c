#include <Python.h>

static PyObject*
spam_strchange(PyObject* self, PyObject* args)
{
	char* str;
	int len = 0;
	if (!PyArg_ParseTuple(args, "s", &str))
		return NULL;
	len = strlen(str);
	for (int i = 0; i < len; i++)
	{
		if (str[i] == '|')
			str[i] = ',';
	}
	str[len - 1] = '\0';
	return Py_BuildValue("s", str);
}

static PyMethodDef SpamMethods[] = {
	{"strchange", spam_strchange, METH_VARARGS,"change character in string"},
	{NULL,NULL,0,NULL}
};

static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",
	"abcdefg",
	-1, SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}
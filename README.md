# Compilador_Jubilo 
<p> Para la correcta ejecución de Júbilo es necesario tener importadas *e instaladas* las siguientes librerías</p>
<p> import numpy as np </p>
<p> import statistics as stats </p>
<p> import math </p>
<p> import matplotlib.pyplot as plt </p>
<p> import pandas as pd </p>
<p> from sklearn.linear_model import LinearRegression </p>

<h3>Quick Reference Manual</h3>

<h2>Tipos de datos</h2>
Int, Float, Bool

<h2>Variables no dimensionadas </h2>

*Declaración de variables*
<p>int x;</p>
<p>float y;</p>
<p>bool flag;</p>

*Declaración de variables con asignación*
<p>int x = 2;</p>
<p>float y = 3.567;</p>
<p>bool flag = True;</p>

<h2> Variables no dimensionadas </h2>

*Declaración de variables*
<p>int matrizX[2][4];</p>
<p>float arregloY[6];</p>

*Declaración de variables con asignación*
<p> int matrixX[2][4] = [[0,1], [2,3], [4,5], [6,7]];</p>
<p> float arregloY[6] = [1.22, 6.5, 3.23, 81.43, 17.65, 7.687];</p>

<h2>Operadores relacionales y lógicos</h2>
<p> == igual a</p>
<p> != diferente a</p>
<p> > mayor que</p>
<p> < menor que</p>
<p> >= mayor o igual que</p>
<= menor o igual que</p>
<p> || or</p>
<p> && and</p>

<h2>Funciones especiales </h2>
<h3>FACT</h3>
<p>Calcula el factorial del valor enviado como parámetro: fact(2)</p>
<p>Parámetro(s) esperados: int mayor a 0 </p>
<p>Tipo de retorno: int </p>

<h3>SUM</h3>
<p>Calcula la sumatoria de un arreglo enviado como parámetro: sum(arregloY) </p>
<p>Parámetro(s) esperados: arreglo de ints o floats </p>
<p>Tipo de retorno: int o float </p>

<h3>MEAN</h3>
<p>Calcula el promedio de un arreglo enviado como parámetro: mean(arregloY) </p>
<p>Parámetro(s) esperados: arreglo de ints o floats </p>
<p>Tipo de retorno: int o float </p>

<h3>MEDIAN</h3>
<p>Calcula la mediana de un arreglo enviado como parámetro: median(arregloY) </p>
<p>Parámetro(s) esperados: arreglo de ints o floats </p>
<p>Tipo de retorno: int o float </p>

<h3>MODE</h3>
<p>Calcula la moda de un arreglo enviado como parámetro: mode(arregloY)</p>
<p>Parámetro(s) esperados: arreglo de ints o floats </p>
<p>Tipo de retorno: int o float </p>

<h3>STDEV</h3>
<p>Calcula la desviación estándar de un arreglo enviado como parámetro: stdev(arregloY)</p>
<p>Parámetro(s) esperados: arreglo de ints o floats </p>
<p>Tipo de retorno: int o float </p>

<h3>VAR</h3>
<p>Calcula la varianza de un arreglo enviado como parámetro: var(arregloY)</p>
<p>Parámetro(s) esperados: arreglo de ints o floats </p>
<p>Tipo de retorno: int o float </p>

<h3>COVARIANCE</h3>
<p>Calcula la covarianza de dos arreglos enviados como parámetros: covariance(arregloX, arregloY)</p>
<p>Parámetro(s) esperados: dos arreglos de ints o floats </p>
<p>Tipo de retorno: int o float </p>

<h3>CORRELATION</h3>
<p>Calcula la correlación de dos arreglos enviados como parámetros: covariance(arregloX, arregloY)</p>
<p>Parámetro(s) esperados: dos arreglos de ints o floats </p>
<p>Tipo de retorno: int o float </p>

<h3>PLOTLINE</h3>
<p>Muestra una gráfica lineal de dos arreglos enviados como parámetros: plotline(arregloX, arregloY</p>
<p>Parámetro(s) esperados: dos arreglos de ints o floats </p>
<p>Tipo de retorno: bool </p>

<h3>PLOTHIST</h3>
<p>Muestra un histograma de un arreglo enviado como parámetro, con el número de bins especificado como segundo parámetro: plothist(arregloX, intX)</p>
<p>Parámetro(s) esperados: un arreglo de ints o floats, una constante entera mayor a 0 </p>
<p>Tipo de retorno: bool </p>

<h3>LINEAREG</h3>
<p>Muestra una gráfica de regresión lineal para dos arreglos enviados como parámetros: lineareg(arregloX, arregloY)</p>
<p>Parámetro(s) esperados: dos arreglos de ints o floats</p>
<p>Tipo de retorno: bool </p>

<h3>SORT</h3>
<p>Ordena los elementos de un arreglo enviado como parámetro: sort(arregloX)</p>
<p>Parámetro(s) esperados: un arreglo de ints o floats</p>
<p>Tipo de retorno: int o float </p>

<h3>TRANSPOSE</h3>
<p>Realiza la transpuesta de una matriz enviada como parámetro: transpose(matrixX)</p>
<p>Parámetro(s) esperados: una matriz de ints o floats</p>
<p>Tipo de retorno: int o float </p>

<h3>EXPORTCSV</h3>
<p>Crea un archivo de tipo csv con el nombre enviado como parámetro. El archivo CSV muestra en forma de dataframe el arreglo o matriz enviado como segundo parámetro : exportcsv('myCSV.csv', matrizX)</p>
<p>Parámetro(s) esperados: constante string, arreglo o matriz de tipo entero o flotante</p>
<p>Tipo de retorno: bool </p>

<h3>EXCHANGE</h3>
<p>Toma dos valores enviados como parámetros (X, Y) y asigna Y a X y X a Y: exchange(x, y)</p>
<p>Parámetro(s) esperados: dos variables no dimensionadas ints o floats </p>
<p>Tipo de retorno: int o float </p>

<h2>Funciones especiales que crean arreglos </h2>
<p>Este tipo de funciones especiales no pueden usarse como operandos </p>

<h3>ARRANGE</h3>
<p>Crea un arreglo desde el límite inferior enviado como parámetro hasta el límite superior enviado como segundo parámetro - 1</p>
<p> EJEMPLO. arregloX -> arrange(2,9) = [2,3,4,5,6,7,8]</p>
<p>Parámetro(s) esperados: dos valores enteros </p>
<p>Tipo de retorno: int </p>

<h3>ZEROS</h3>
<p>Crea un arreglo de 0s del tamaño enviado como parámetro </p>
<p> EJEMPLO. arregloX -> zeros(7) = [0,0,0,0,0,0,0]</p>
<p>Parámetro(s) esperados: un valor entero mayor a 0 </p>
<p>Tipo de retorno: int </p>

<h3>ONES</h3>
<p>Crea un arreglo de 1s del tamaño enviado como parámetro </p>
<p> EJEMPLO. arregloX -> zeros(7) = [1,1,1,1,1,1,1]</p>
<p>Parámetro(s) esperados: un valor entero mayor a 0 </p>
<p>Tipo de retorno: int </p>

<h3>RANDINT</h3>
<p>Crea un arreglo de enteros aleatorios desde el límite inferior enviado como parámetro hasta el límite superior enviado como segundo parámetro, el tamaño del arreglo está definido por el tercer parámetro </p>
<p> EJEMPLO. arregloX -> randint(0, 20, 5) = [18, 4, 7, 16, 2]</p>
<p>Parámetro(s) esperados: valor entero, valor entero, constante entera </p>
<p>Tipo de retorno: int </p>

<h3>RANDFLOAT</h3>
<p>Crea un arreglo de enteros aleatorios desde el límite inferior enviado como parámetro hasta el límite superior enviado como segundo parámetro, el tamaño del arreglo está definido por el tercer parámetro </p>
<p> EJEMPLO. arregloX -> randfloat(2.2, 20.5, 5) = [18.34, 12.54, 8.53, 3.45, 2.23]</p>
<p>Parámetro(s) esperados: valor entero o flotante, valor entero o flotante, constante entera </p>
<p>Tipo de retorno: float</p>



















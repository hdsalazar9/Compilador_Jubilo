# Compilador_Jubilo 
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













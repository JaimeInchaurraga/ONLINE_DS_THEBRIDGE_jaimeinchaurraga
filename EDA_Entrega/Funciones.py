import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# GRÁFICO DE BARRAS COLUMNAS CATEGÓRICAS CORE
# He tenido que realizar una serie de modificaciones en la función para poder controlar mejor el formato de las gráficas y poder gestionar el número de resultados a mostrar

# función modificada para pintar gráficos de barras aprovechando al máximo el ancho y altura disponibles
def pinta_distribucion_categoricas(df, columnas_categoricas, relativa=False, mostrar_valores=False, top_n=None):
    num_columnas = len(columnas_categoricas)
    num_filas = (num_columnas // 2) + (num_columnas % 2)

    # Aumentar el ancho y la altura del gráfico para aprovechar todo el espacio disponible
    # Ajusta el valor 60 (ancho) y 10 (altura) de figsize según sea necesario
    fig, axes = plt.subplots(num_filas, 2, figsize=(60, 20 * num_filas))  # Ajustar aquí para ancho y altura
    axes = axes.flatten()

    for i, col in enumerate(columnas_categoricas):
        ax = axes[i]
        serie = df[col].value_counts().nlargest(top_n) if top_n else df[col].value_counts()

        if relativa:
            total = serie.sum()
            serie = serie.apply(lambda x: x / total)
            ax.set_ylabel('Frecuencia Relativa')
        else:
            ax.set_ylabel('Frecuencia')

        sns.barplot(x=serie.index, y=serie, ax=ax, palette='viridis', hue=serie.index, legend=False)

        ax.set_title(f'Distribución de {col}')
        ax.set_xlabel('')
        ax.tick_params(axis='x', rotation=45)

        if mostrar_valores:
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height), 
                            ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    # Desactivar los ejes no utilizados para una visualización más limpia
    for j in range(i + 1, num_filas * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

def variabilidad(df):
    df_var = df.describe().loc[["std", "mean"]].T
    df_var["CV"] = df_var["std"] / df_var["mean"]

    # Formatear la columna 'CV' como porcentaje
    format_dict = {'CV': '{:.2%}'} # formato de cadena que convierte los números en un formato de porcentaje con dos decimales
    return df_var.style.format(format_dict)

# Función para ver todos los histogramas de las variables numéricas

def plot_histograms(df, numeric_columns):
    num_plots = len(numeric_columns)
    num_cols = 2
    num_rows = num_plots // num_cols + (num_plots % num_cols > 0)
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10 * num_cols, 5 * num_rows))
    axes = axes.ravel()

    for i, col in enumerate(numeric_columns):
        ax = axes[i]
        df[col].hist(ax=ax)
        ax.set_title(f'Histograma de {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Frecuencia')

    # Si el número de subgráficos no llena completamente la cuadrícula, ocultamos los ejes sobrantes.
    for j in range(i+1, num_rows*num_cols):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def plot_multiple_boxplots(df, columns, dim_matriz_visual=2, log_scale=False):
    num_cols = len(columns)
    num_rows = num_cols // dim_matriz_visual + (num_cols % dim_matriz_visual > 0)
    fig, axes = plt.subplots(num_rows, dim_matriz_visual, figsize=(12, 8 * num_rows))  # Aumentamos la altura para cada fila
    axes = axes.flatten() if num_rows > 1 else [axes]

    for i, column in enumerate(columns):
        if df[column].dtype in ['int64', 'float64']:
            sns.boxplot(data=df, x=column, ax=axes[i], showfliers=True, medianprops={'color': 'orange'}) # añado una variable que permite cambiar el color para visualizar mejor la mediana
            axes[i].set_title(column)
            # Aplicar escala logarítmica si se especifica y los datos lo permiten (valores > 0)
            if log_scale and (df[column] > 0).all():
                axes[i].set_xscale('log')

    # Ocultar ejes vacíos
    for j in range(i+1, num_rows * dim_matriz_visual):
        if j < len(axes):
            axes[j].axis('off')

    plt.tight_layout()
    plt.show()





# Esta nueva versión de la función permite añadir diferentes columnas de diferentes Dataframes (debido que al explotar ciertas columnas tuve que crear dataframes distintos)
# ahora acepta una lista de duplas, donde cada dupla es un DataFRame y el nombre de la columnas a pintar
def pinta_distribucion_categoricas_dfs_mixtos(columnas_categoricas, relativa=False, mostrar_valores=False, top_n=None):
    num_columnas = len(columnas_categoricas)
    num_filas = (num_columnas // 2) + (num_columnas % 2)

    fig, axes = plt.subplots(num_filas, 2, figsize=(60, 20 * num_filas))  # Ajustar aquí para ancho y altura
    axes = axes.flatten()

    for i, (df, col) in enumerate(columnas_categoricas):
        ax = axes[i]
        serie = df[col].value_counts().nlargest(top_n) if top_n else df[col].value_counts()

        if relativa:
            total = serie.sum()
            serie = serie.apply(lambda x: x / total)
            ax.set_ylabel('Frecuencia Relativa')
        else:
            ax.set_ylabel('Frecuencia')

        sns.barplot(x=serie.index, y=serie, ax=ax, palette='viridis', hue=serie.index, legend=False)

        ax.set_title(f'Distribución de {col}')
        ax.set_xlabel('')
        ax.tick_params(axis='x', rotation=45)

        if mostrar_valores:
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height), 
                            ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    for j in range(i + 1, num_filas * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()



def plot_interactive_comparison_categorica(df1, col1, df2, col2, id_col, top_n=10, relative=False):
    # Conteo de las categorías en df1
    top_categories_df1 = df1[col1].value_counts().nlargest(top_n).index
    df1 = df1[df1[col1].isin(top_categories_df1)]
    
    # Conteo de categorías en df2
    top_categories_df2 = df2[col2].value_counts().nlargest(top_n).index
    df2 = df2[df2[col2].isin(top_categories_df2)]
    
    # Unir los dos DataFrames en la columna común id_col
    merged_df = pd.merge(df1[[id_col, col1]], df2[[id_col, col2]], on=id_col, how='inner')
    
    # Calcular las frecuencias de las categorías de col2 dentro de cada categoría de col1
    category_counts = merged_df.groupby([col1, col2]).size().unstack(fill_value=0)
    if relative:
        category_counts = category_counts.div(category_counts.sum(axis=1), axis=0)
    
    # Ordenar los elementos de la leyenda por la suma total en col2
    col2_sorted = category_counts.sum(axis=0).nlargest(top_n).index
    
    # Graficar
    figsize = (15, 10)  # Tamaño del gráfico
    ax = category_counts[col2_sorted].plot(kind='bar', stacked=True, figsize=figsize, colormap='tab20')
    
    # Etiquetas y títulos
    ax.set_title(f'Top {top_n} Categories in {col1} and their distribution in {col2}')
    ax.set_xlabel(col1)
    ax.set_ylabel('Percentage' if relative else 'Count')
    
    # Ordenar la leyenda
    handles, labels = ax.get_legend_handles_labels()
    handles = [handles[labels.index(label)] for label in col2_sorted if label in labels]
    ax.legend(handles, col2_sorted, title=col2, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    plt.tight_layout()
    plt.show()

# Ejemplo de uso
# plot_interactive_comparison_dos(df_exploded_genres, 'Genres', df_exploded_team, 'Team', 'GameID', top_n=15, relative=False)




def plot_interactive_comparison_continua(df1, col1, df2, col2, id_col, top_n=10, relative=False):
    # Conteo de las categorías en df1
    top_categories_df1 = df1[col1].value_counts().nlargest(top_n).index
    df1 = df1[df1[col1].isin(top_categories_df1)]
    
    # Conteo de categorías en df2
    top_categories_df2 = df2[col2].value_counts().nlargest(top_n).index
    df2 = df2[df2[col2].isin(top_categories_df2)]
    
    # Unir los dos DataFrames en la columna común id_col
    merged_df = pd.merge(df1[[id_col, col1]], df2[[id_col, col2]], on=id_col, how='inner')
    
    # Calcular las frecuencias de las categorías de col2 dentro de cada categoría de col1
    category_counts = merged_df.groupby([col1, col2]).size().unstack(fill_value=0)
    if relative:
        # Convertir conteos a proporciones
        category_counts = category_counts.div(category_counts.sum(axis=1), axis=0)
    
    # Ajustar el tamaño del gráfico basado en top_n para evitar superposición
    width_per_bar = 0.5  # Ajustar según sea necesario
    fig_width = max(15, top_n * width_per_bar)
    fig_height = 10  # Ajustar según sea necesario
    figsize = (fig_width, fig_height)
    
    # Graficar
    ax = category_counts.plot(kind='bar', stacked=True, figsize=figsize, colormap='viridis')
    
    # Etiquetas y títulos
    ax.set_title(f'Top {top_n} Categories in {col1} and their distribution in {col2}')
    ax.set_xlabel(col1)
    ax.set_ylabel('Percentage' if relative else 'Count')
    ax.legend(title=col2, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Ajustar la rotación y la alineación de las etiquetas del eje X
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    plt.tight_layout()
    plt.show()


# plot_interactive_comparison(df_exploded_1, 'Category1', df_exploded_2, 'Category2', 'GameID', top_n=10, relative=True)


def plot_interactive_comparison_discreta(df1, col1, df2, col2, id_col, top_n=10, bins_range=None):
    if bins_range is None:
        bins_range = [0, 500, 1000, 5000, 10000, 50000, 100000, np.inf]

    top_categories_df1 = df1[col1].value_counts().nlargest(top_n).index
    df1_filtered = df1[df1[col1].isin(top_categories_df1)]

    df2['range'] = pd.cut(df2[col2], bins=bins_range, labels=[f'{bins_range[i]}-{bins_range[i+1]-1}' for i in range(len(bins_range)-1)], right=False)
    merged_df = pd.merge(df1_filtered[[id_col, col1]], df2[[id_col, 'range']], on=id_col, how='inner')

    category_counts = merged_df.groupby([col1, 'range']).size().unstack(fill_value=0)
    category_counts = category_counts.div(category_counts.sum(axis=1), axis=0)

    # Ajustar el tamaño del gráfico basado en top_n
    fig_width = max(15, top_n)  # Aumentar el ancho si top_n es grande
    fig_height = 10
    figsize = (fig_width, fig_height)

    ax = category_counts.plot(kind='bar', stacked=True, figsize=figsize, colormap='tab20')
    ax.set_title(f'Top {top_n} Categories in {col1} and their distribution in {col2}')
    ax.set_xlabel(col1)
    ax.set_ylabel('Relative Frequency')
    ax.legend(title='Plays Range', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Rotar las etiquetas del eje X para mejorar la legibilidad
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


# plot_interactive_comparison_discrete(df_exploded_genres, 'Genres', df, 'Plays', 'GameID', top_n=50, bins_range=[0, 500, 1000, 5000, 10000, 50000, 100000, np.inf])


# igual que la primera versión pero esta me permite trabajar con frecuencias ABSOLUTAS
def plot_interactive_comparison_discreta_dos(df1, col1, df2, col2, id_col, top_n=10, bins_range=None, relative=True):
    if bins_range is None:
        bins_range = [0, 500, 1000, 5000, 10000, 50000, 100000, np.inf]

    top_categories_df1 = df1[col1].value_counts().nlargest(top_n).index
    df1_filtered = df1[df1[col1].isin(top_categories_df1)]

    df2['range'] = pd.cut(df2[col2], bins=bins_range, labels=[f'{bins_range[i]}-{bins_range[i+1]-1}' for i in range(len(bins_range)-1)], right=False)
    merged_df = pd.merge(df1_filtered[[id_col, col1]], df2[[id_col, 'range']], on=id_col, how='inner')

    category_counts = merged_df.groupby([col1, 'range']).size().unstack(fill_value=0)
    if relative:
        category_counts = category_counts.div(category_counts.sum(axis=1), axis=0)

    fig_width = max(15, top_n)  # Aumentar el ancho si top_n es grande
    fig_height = 10
    figsize = (fig_width, fig_height)

    ax = category_counts.plot(kind='bar', stacked=True, figsize=figsize, colormap='tab20')
    ax.set_title(f'Top {top_n} Categories in {col1} and their distribution in {col2}')
    ax.set_xlabel(col1)
    ax.set_ylabel('Relative Frequency' if relative else 'Total Count')
    ax.legend(title=col2 + ' Range', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def grafico_dispersion_con_correlacion(df, columna_x, columna_y, tamano_puntos=50, mostrar_correlacion=False):
    """
    Crea un diagrama de dispersión entre dos columnas y opcionalmente muestra la correlación.

    Args:
    df (pandas.DataFrame): DataFrame que contiene los datos.
    columna_x (str): Nombre de la columna para el eje X.
    columna_y (str): Nombre de la columna para el eje Y.
    tamano_puntos (int, opcional): Tamaño de los puntos en el gráfico. Por defecto es 50.
    mostrar_correlacion (bool, opcional): Si es True, muestra la correlación en el gráfico. Por defecto es False.
    """

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=columna_x, y=columna_y, s=tamano_puntos)

    if mostrar_correlacion:
        correlacion = df[[columna_x, columna_y]].corr().iloc[0, 1]
        plt.title(f'Diagrama de Dispersión con Correlación: {correlacion:.2f}')
    else:
        plt.title('Diagrama de Dispersión')

    plt.xlabel(columna_x)
    plt.ylabel(columna_y)
    plt.grid(True)
    plt.show()

from scipy.stats import chi2_contingency
import pandas as pd

def test_chi_cuadrado_dfs_exploded(df1, columna_df1, df2, columna_df2, columna_id_comun):
    """
    Realiza el test de chi-cuadrado para dos columnas de dos DataFrames diferentes y
    imprime los resultados.

    Parámetros:
    df1 : primer DataFrame
    columna_df1 : la columna del primer DataFrame para la prueba
    df2 : segundo DataFrame
    columna_df2 : la columna del segundo DataFrame para la prueba
    columna_id_comun : el nombre de la columna común para hacer la fusión de los DataFrames
    """

    # Realiza la fusión de los DataFrames en la columna de identificación común
    merged_df = pd.merge(df1[[columna_id_comun, columna_df1]], df2[[columna_id_comun, columna_df2]], on=columna_id_comun)

    # Crea la tabla de contingencia para las dos columnas especificadas
    tabla_contingencia = pd.crosstab(merged_df[columna_df1], merged_df[columna_df2])

    # Realizar el test de chi-cuadrado
    chi2, p, dof, expected = chi2_contingency(tabla_contingencia)

    # Imprime los resultados
    print("Valor Chi-Cuadrado:", chi2)
    print("P-Value:", p)
    print("Grados de Libertad:", dof)
    print("\nTabla de Frecuencias Esperadas:\n", expected)










'''

Si estás observando que todas las barras llegan a 1.0 en el modo relativo (relative=True), incluso cuando estás mostrando un top_n limitado de equipos, 
esto sugiere que la normalización de los datos se está realizando de tal manera que la suma de las contribuciones de los equipos dentro de cada género es igual a 1.0 para cada género.
Cuando relative=True, lo que la función intenta mostrar es la distribución porcentual de los equipos dentro de cada género individualmente. 
Es decir, para cada género, la suma de las contribuciones de todos los equipos mostrados (en este caso, los 15 equipos principales) sumará 1.0 o 100%. 
Esto no significa que estés viendo todos los equipos existentes en el dataset, sino más bien cómo se distribuyen los equipos principales dentro de cada género específico.

Por ejemplo, si el género "Aventura" tiene juegos de 15 equipos diferentes, y estás mostrando el top 15, la función muestra qué porcentaje del total de juegos de "Aventura" (dentro de ese top 15) pertenece a cada equipo. Si un equipo tiene un 30% de los juegos de "Aventura", su barra en el gráfico de "Aventura" representará el 30% de la altura total de esa barra específica.
'''

'''
esta función ordena las categorías de la leyenda en orden de mayor a menor según su frecuencia absoluta
'''


'''
    a función plot_interactive_comparison_dos calcula la frecuencia de los equipos (col2) dentro de cada categoría de géneros (col1) y luego suma estas frecuencias para ordenar la leyenda. 
    Esto significa que si un equipo, como Capcom, tiene una distribución más amplia a través de varios géneros, podría aparecer más alto en la leyenda, incluso si el número total de juegos es menor que el de Sega.
Limitación por top_n: La función limita tanto las categorías de géneros como los equipos a los top_n más frecuentes. Si Sega no está presente en tantos géneros como Capcom dentro de los top_n géneros, 
eso podría explicar por qué Capcom aparece antes en la leyenda.

'''
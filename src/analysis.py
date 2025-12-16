import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_and_reshape_data(filepath):
    """Carga los datos y los remodela para el análisis."""
    df = pd.read_csv(filepath)
    
    # Limpiar nombres de columnas (eliminar espacios en blanco)
    df.columns = df.columns.str.strip()

    # Renombrar columnas para que sea más fácil trabajar con ellas
    df.rename(columns={
        'Phenomenon_Type': 'Phenomenon',
        'S1_Sum_TIF': 'S1_Sum'
    }, inplace=True)

    # Extraer los datos de las estrategias S1, S2, S3
    s1 = df[['Phenomenon', 'Model', 'S1_Truth_T', 'S1_Indet_I', 'S1_Falsity_F', 'S1_Sum']].copy()
    s1['Strategy'] = 'S1 (Neutrosophic)'
    s1.rename(columns={'S1_Truth_T': 'Truth', 'S1_Indet_I': 'Indeterminacy', 'S1_Falsity_F': 'Falsity', 'S1_Sum': 'Sum'}, inplace=True)

    s2 = df[['Phenomenon', 'Model', 'S2_Truth_T', 'S2_Indet_I', 'S2_Falsity_F']].copy()
    s2['Strategy'] = 'S2 (Probabilistic)'
    s2['Sum'] = s2['S2_Truth_T'] + s2['S2_Indet_I'] + s2['S2_Falsity_F']
    s2.rename(columns={'S2_Truth_T': 'Truth', 'S2_Indet_I': 'Indeterminacy', 'S2_Falsity_F': 'Falsity'}, inplace=True)
    
    # Combinar los dataframes
    reshaped_df = pd.concat([s1, s2], ignore_index=True)
    
    return reshaped_df

def plot_components_distribution(df, output_path):
    """Genera y guarda el gráfico de distribución de componentes neutrosóficos."""
    df_s1 = df[df['Strategy'] == 'S1 (Neutrosophic)']
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=df_s1, x='Phenomenon', y='Truth', hue='Model')
    plt.title('Distribución del Componente Verdad (T) en el Framework Neutrosófico (S1)', fontsize=16)
    plt.xticks(rotation=25, ha='right')
    plt.xlabel('Fenómeno Lingüístico')
    plt.ylabel('Valor de Verdad (T)')
    plt.legend(title='Modelo')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_hypertruth_sum(df, output_path):
    """Genera y guarda el gráfico de la suma de componentes (Hiper-Verdad)."""
    df_s1 = df[df['Strategy'] == 'S1 (Neutrosophic)']
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=df_s1, x='Phenomenon', y='Sum', hue='Model')
    plt.title('Suma de Componentes (T+I+F) en el Framework Neutrosófico (S1)', fontsize=16)
    plt.axhline(y=1.0, color='r', linestyle='--', label='Límite Probabilístico (Suma=1)')
    plt.xticks(rotation=25, ha='right')
    plt.xlabel('Fenómeno Lingüístico')
    plt.ylabel('Suma de Componentes')
    plt.legend(title='Modelo')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_s1_vs_s2_comparison(df, output_path):
    """Genera y guarda el gráfico de comparación entre Estrategia 1 y 2."""
    plt.figure(figsize=(14, 8))
    sns.barplot(data=df, x='Phenomenon', y='Truth', hue='Strategy', palette=['#4338CA', '#818CF8'])
    plt.title('Comparación del Valor de Verdad (T): Neutrosófico vs. Probabilístico', fontsize=16)
    plt.xticks(rotation=25, ha='right')
    plt.xlabel('Fenómeno Lingüístico')
    plt.ylabel('Valor de Verdad Promedio (T)')
    plt.legend(title='Estrategia')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_model_performance(df, output_path):
    """Genera y guarda el gráfico de rendimiento por modelo."""
    df_s1 = df[df['Strategy'] == 'S1 (Neutrosophic)']
    plt.figure(figsize=(12, 8))
    sns.violinplot(data=df_s1, x='Model', y='Sum', inner='quartile', palette='viridis')
    plt.title('Distribución de la Suma de Componentes por Modelo (Framework Neutrosófico)', fontsize=16)
    plt.xlabel('Modelo')
    plt.ylabel('Suma de Componentes (T+I+F)')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_correlation_heatmap(df, output_path):
    """Genera y guarda el mapa de calor de correlaciones."""
    df_s1 = df[df['Strategy'] == 'S1 (Neutrosophic)']
    corr = df_s1[['Truth', 'Indeterminacy', 'Falsity', 'Sum']].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
    plt.title('Matriz de Correlación de Componentes Neutrosóficos (S1)', fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_ethical_contradiction(df, output_path):
    """Genera y guarda el gráfico para el análisis de contradicción ética."""
    df_ethical = df[(df['Phenomenon'] == 'Contradiction (Ethical)') & (df['Strategy'] == 'S1 (Neutrosophic)')]
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df_ethical, x='Truth', y='Falsity', hue='Model', size='Indeterminacy', sizes=(100, 1000), palette='magma', alpha=0.7)
    plt.title('Análisis de Contradicción Ética (Framework Neutrosófico)', fontsize=16)
    plt.xlabel('Valor de Verdad (T)')
    plt.ylabel('Valor de Falsedad (F)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title='Modelo y Nivel de Indeterminación')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == '__main__':
    # Asegurarse de que el directorio de resultados exista
    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    data_path = 'data/openai_neutrosophic_results.csv'
    
    # Cargar y remodelar los datos
    reshaped_df = load_and_reshape_data(data_path)
    
    # Generar todos los gráficos
    print("Generando gráficos...")
    plot_components_distribution(reshaped_df, os.path.join(results_dir, 'fig1_components_distribution.png'))
    plot_hypertruth_sum(reshaped_df, os.path.join(results_dir, 'fig2_hypertruth_sum.png'))
    plot_s1_vs_s2_comparison(reshaped_df, os.path.join(results_dir, 'fig3_s1_vs_s2_comparison.png'))
    plot_model_performance(reshaped_df, os.path.join(results_dir, 'fig4_model_performance.png'))
    plot_correlation_heatmap(reshaped_df, os.path.join(results_dir, 'fig5_correlation_heatmap.png'))
    plot_ethical_contradiction(reshaped_df, os.path.join(results_dir, 'fig6_ethical_contradiction.png'))
    
    print(f'Análisis completado. {len(os.listdir(results_dir))} gráficos guardados en {results_dir}/')

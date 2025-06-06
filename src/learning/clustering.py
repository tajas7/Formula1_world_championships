import pandas as pd
from functools import reduce
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def cluster_driving_styles(save_outputs=False):
    """
    Performs unsupervised clustering on F1 drivers based on various performance metrics
    - loads multiple datasets
    - computes a variety of performance indicators
    - applies standardization
    - uses KMeans clustering
    - visualizes the results with PCA

    Can export :
    - elbow_method.png: chart showing inertia relatively to the number of clusters
    - pca_visualization.png: scatter plot of PCA-transformed clusters
    - pca_contributions.csv: variable contributions to PCA components
    - clusters.csv: driver names grouped by cluster

    Parameters
    ----------
    save_outputs : bool
        If True, saves the visualizations and tables

    Returns
    -------
    None : results are either visualized or exported to files

    """
    # Load data
    drivers = pd.read_csv('./data/drivers.csv')
    results = pd.read_csv('./data/results.csv')
    status = pd.read_csv('./data/status.csv')
    lap_times = pd.read_csv('./data/lap_times.csv')
    pit_stops = pd.read_csv('./data/pit_stops.csv')
    qualifying = pd.read_csv('./data/qualifying.csv')

    # Cleaning types
    results['positionOrder'] = pd.to_numeric(results['positionOrder'], errors='coerce')
    results['grid'] = pd.to_numeric(results['grid'], errors='coerce')
    results['statusId'] = pd.to_numeric(results['statusId'], errors='coerce')

    # New variables
    win_rate = (
        results.groupby('driverId')['positionOrder'].apply(lambda x: (x == 1).mean())
                                                    .reset_index(name='win_rate')
    )
    podium_rate = (
        results.groupby('driverId')['positionOrder'].apply(lambda x: (x <= 3).mean())
                                                    .reset_index(name='podium_rate')
    )

    finished_ids = (
        status[status['status'].str.contains(r'Finished|\+')]['statusId'].astype(int)
    )

    results['finished'] = results['statusId'].isin(finished_ids)
    finish_rate = (
        results.groupby('driverId')['finished'].mean().reset_index(name='finish_rate')
    )

    results['position_gain'] = results['grid'] - results['positionOrder']
    avg_position_gain = (
        results.groupby('driverId')['position_gain'].mean()
                                                    .reset_index(
                                                        name='avg_position_gain')
    )

    lap_stats = (
        lap_times.groupby('driverId')['milliseconds'].agg(avg_lap_time='mean',
                                                          std_lap_time='std')
                                                     .reset_index()
    )

    for q in ['q1', 'q2', 'q3']:
        qualifying[q] = pd.to_numeric(qualifying[q], errors='coerce')
    qualifying['mean_qualifying_position'] = qualifying[['q1', 'q2', 'q3']].mean(axis=1)
    mean_qual = (
        qualifying.groupby('driverId')['mean_qualifying_position'].mean().reset_index()
    )

    pit_stops['pit_time'] = pit_stops['milliseconds']
    pit_agg = (
        pit_stops.groupby('driverId')['pit_time'].agg(avg_pit_stop_time='mean',
                                                      avg_pit_stop_count='count')
                                                 .reset_index()
    )

    dfs = [avg_position_gain, win_rate, podium_rate,
           finish_rate, lap_stats, mean_qual, pit_agg]
    df_pilotes = reduce(lambda left, right: pd.merge(left, right,
                                                     on='driverId', how='outer'), dfs)
    df_pilotes = df_pilotes.merge(drivers[['driverId', 'forename', 'surname']],
                                  on='driverId', how='left')
    df_pilotes['name'] = df_pilotes['forename'] + ' ' + df_pilotes['surname']

    mean_race_pos = (
        results.groupby('driverId')['positionOrder'].mean()
                                                    .reset_index(
                                                        name='mean_race_position')
    )

    qualif_vs_race = mean_race_pos.merge(mean_qual, on='driverId')
    qualif_vs_race['qualif_vs_race_delta'] = (
        qualif_vs_race['mean_qualifying_position'] -
        qualif_vs_race['mean_race_position']
    )

    position_std = (
        results.groupby('driverId')['positionOrder'].std()
                                                    .reset_index(name='position_std')
    )

    results['is_podium'] = results['positionOrder'] <= 3
    results['is_finished'] = results['statusId'].isin(finished_ids)
    filtered = results[results['is_finished']]
    podium_when_finished = (
        filtered.groupby('driverId')['is_podium'].mean()
                                                 .reset_index(
                                                     name='podium_when_finished_rate')
    )

    vars_to_merge = [qualif_vs_race[['driverId', 'qualif_vs_race_delta']],
                     position_std, podium_when_finished]
    for df in vars_to_merge:
        df_pilotes = df_pilotes.merge(df, on='driverId', how='left')

    df_pilotes = df_pilotes.fillna(0)

    # Kmeans
    features = df_pilotes.drop(columns=['driverId', 'forename', 'surname', 'name'])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Elbow method
    inertias = []
    for k in range(1, 11):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(X_scaled)
        inertias.append(model.inertia_)

    plt.figure(figsize=(8, 6))
    plt.plot(range(1, 11), inertias, marker='o')
    plt.title("Elbow method")
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    plt.grid(True)
    plt.tight_layout()
    if save_outputs:
        plt.savefig("elbow_method.png")
    plt.gcf()
    plt.close()

    # Final clustering with k = 3
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_pilotes['cluster'] = kmeans.fit_predict(X_scaled)

    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    df_pilotes['PCA1'] = X_pca[:, 0]
    df_pilotes['PCA2'] = X_pca[:, 1]

    # PCA Visualization
    plt.figure(figsize=(8, 6))
    for cluster_id in df_pilotes['cluster'].unique():
        cluster_data = df_pilotes[df_pilotes['cluster'] == cluster_id]
        plt.scatter(cluster_data['PCA1'],
                    cluster_data['PCA2'],
                    label=f'Cluster {cluster_id}',
                    alpha=0.6)

    plt.title("Projection PCA des pilotes par cluster")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save_outputs:
        plt.savefig("pca_visualization.png")
    plt.gcf()
    plt.close()

    # Variables' contributions to PCA
    pca_contrib = pd.DataFrame(pca.components_.T,
                               index=features.columns,
                               columns=['PC1', 'PC2'])
    if save_outputs:
        pca_contrib.to_csv("pca_contributions.csv")

    # Clusters' composition
    clusters = df_pilotes.groupby('cluster')['name'].apply(list).to_dict()
    max_len = max(len(names) for names in clusters.values())
    cluster_table = pd.DataFrame({
        f'Cluster {i}': (clusters.get(i, [])
                         + [''] * (max_len - len(clusters.get(i, []))))
        for i in sorted(clusters.keys())
    })
    if save_outputs:
        cluster_table.to_csv("clusters.csv", index=False)

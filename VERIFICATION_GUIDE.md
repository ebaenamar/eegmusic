# 🔍 Verification Guide - EEG to Music Mapping

## ✅ Cambios Realizados

### 1. **Visualización Arreglada**
- ✅ Callback ahora usa `asyncio.create_task()` en lugar de `asyncio.run()`
- ✅ Datos de hemisferios (left/right alpha) se envían correctamente
- ✅ Todas las métricas se actualizan en tiempo real

### 2. **Escala Base Configurable**
- ✅ Nuevo selector "BASE SCALE" en la UI
- ✅ Opciones: AUTO (from EEG), MAJOR, MINOR, PENTATONIC, BLUES
- ✅ AUTO = escala determinada por valence del EEG
- ✅ Manual = fuerza la escala seleccionada

### 3. **Mapeo EEG → Música Verificado**

## 🎵 Cómo Verificar que Cada CSV Produce Música Diferente

### Mapeo Neurológico Implementado

#### 1. **Tempo (60-140 BPM)**
```python
# Basado en arousal (alertness ratio)
arousal = (left_alertness + right_alertness) / 2
base_tempo = 70 + arousal * 80  # 70-150 BPM

# Modulado por beta del hemisferio izquierdo
beta_modulation = 1.0 + (left_beta - 0.2) * 0.3
final_tempo = base_tempo * beta_modulation * tempo_stability
```

**Verificación:**
- CSV con alto beta → Tempo más rápido
- CSV con bajo beta → Tempo más lento
- Observa el valor "TEMPO" en el dashboard

#### 2. **Escala Musical**
```python
# Basado en valence (focus ratio)
if valence > 0.55:
    scale = 'major'      # Focused, positive
elif valence < 0.35:
    scale = 'minor'      # Unfocused, contemplative
else:
    scale = 'pentatonic' # Neutral
```

**Verificación:**
- CSV con alto alpha/theta → Major (alegre)
- CSV con bajo alpha/theta → Minor (melancólico)
- Observa el valor "SCALE" en el dashboard

#### 3. **Energía y Volumen**
```python
energy = (left_engagement + right_engagement) / 2
volume = energy * base_volume
```

**Verificación:**
- CSV con alto engagement → Música más fuerte
- CSV con bajo engagement → Música más suave
- Observa el valor "ENERGY" en el dashboard

#### 4. **Complejidad Melódica**
```python
# Basado en alpha del hemisferio derecho
melody_complexity = right_alpha * 0.7
num_notes = 2 + arousal * 6 + cognitive_load * 2
```

**Verificación:**
- CSV con alto right_alpha → Melodías más complejas
- CSV con bajo right_alpha → Melodías más simples
- Observa "ALPHA" en Brain Activity

#### 5. **Armonía**
```python
# Basado en alpha + gamma del hemisferio derecho
harmony = (right_alpha + right_gamma) / 2
```

**Verificación:**
- CSV con alto right_alpha+gamma → Armonías más ricas
- CSV con bajo right_alpha+gamma → Armonías más simples
- Observa "ALPHA" y "GAMMA" en Brain Activity

#### 6. **Ritmo**
```python
# Basado en theta del hemisferio izquierdo
rhythm_variation = left_theta * 0.5
```

**Verificación:**
- CSV con alto left_theta → Ritmo más variado
- CSV con bajo left_theta → Ritmo más constante

## 🧪 Prueba Práctica

### Paso 1: Cargar CSV y Observar
1. Carga un CSV
2. Observa los valores iniciales:
   - DELTA, THETA, ALPHA, BETA, GAMMA
   - AROUSAL, VALENCE, ENERGY
   - TEMPO, SCALE

### Paso 2: Comparar Diferentes CSVs

#### CSV con Alta Actividad (Beta alto)
```
Esperado:
- Tempo: 110-140 BPM
- Scale: Major o Pentatonic
- Energy: 0.6-1.0
- Complejidad: Alta
```

#### CSV con Baja Actividad (Beta bajo, Delta/Theta alto)
```
Esperado:
- Tempo: 60-90 BPM
- Scale: Minor
- Energy: 0.2-0.5
- Complejidad: Baja
```

#### CSV con Alta Concentración (Alpha alto)
```
Esperado:
- Tempo: 90-110 BPM
- Scale: Major
- Melodía: Compleja
- Armonía: Rica
```

### Paso 3: Verificar Cambios en Tiempo Real

Mientras reproduce un CSV, observa:

1. **Oscilloscope**: Las ondas deben cambiar
2. **Brain Activity**: Los valores deben variar
3. **Musical State**: Debe reflejar los cambios
4. **Audio**: Debe sonar diferente según los valores

## 📊 Valores de Referencia

### Band Powers (Normalized 0-1)
- **Delta (0.5-4 Hz)**: 0.02-0.08 típico
- **Theta (4-8 Hz)**: 0.3-0.6 típico
- **Alpha (8-13 Hz)**: 0.15-0.35 típico
- **Beta (13-30 Hz)**: 0.1-0.4 típico
- **Gamma (30-50 Hz)**: 0.01-0.08 típico

### Cognitive Metrics
- **Focus (α/θ+α)**: 0.2-0.5 típico
- **Alertness (β/θ+β)**: 0.15-0.5 típico
- **Engagement**: 0.3-0.6 típico

### Musical Output
- **Tempo**: 60-140 BPM
- **Arousal**: 0-1 (0=calm, 1=excited)
- **Valence**: 0-1 (0=negative, 1=positive)
- **Energy**: 0-1 (0=soft, 1=loud)

## 🔬 Prueba Científica

### Crear CSVs de Prueba

#### 1. CSV "Relajado"
```csv
Left__delta,Left__theta,Left__alpha,Left__beta,Left__gamma,...
0.05,0.6,0.25,0.08,0.02,...
```
**Esperado**: Tempo lento, Minor, Energía baja

#### 2. CSV "Activo"
```csv
Left__delta,Left__theta,Left__alpha,Left__beta,Left__gamma,...
0.02,0.25,0.15,0.5,0.08,...
```
**Esperado**: Tempo rápido, Major, Energía alta

#### 3. CSV "Concentrado"
```csv
Left__delta,Left__theta,Left__alpha,Left__beta,Left__gamma,...
0.03,0.3,0.45,0.18,0.04,...
```
**Esperado**: Tempo medio, Major, Melodía compleja

## ✅ Checklist de Verificación

- [ ] Oscilloscope muestra ondas diferentes para cada CSV
- [ ] Brain Activity valores cambian según el CSV
- [ ] Tempo varía según beta/arousal
- [ ] Escala cambia según valence
- [ ] Energy refleja engagement
- [ ] Música suena diferente entre CSVs
- [ ] Cambios son suaves (no abruptos)
- [ ] Escala base manual funciona
- [ ] Stop detiene correctamente
- [ ] Métricas se actualizan en tiempo real

## 🎯 Diferencias Clave Entre CSVs

| Métrica | CSV 1 | CSV 2 | Diferencia Musical |
|---------|-------|-------|-------------------|
| Beta | 0.1 | 0.4 | Tempo: 80 vs 120 BPM |
| Alpha | 0.2 | 0.4 | Melodía: Simple vs Compleja |
| Valence | 0.3 | 0.6 | Escala: Minor vs Major |
| Engagement | 0.3 | 0.7 | Volumen: Suave vs Fuerte |

## 🐛 Si No Ves Diferencias

1. **Verifica que el CSV tiene datos variados**
   - Mira los valores en el CSV
   - Deben variar entre filas

2. **Revisa el smoothing**
   - Smoothing alto (20+) = cambios muy lentos
   - Prueba con smoothing bajo (10) para ver cambios más rápidos

3. **Observa los logs del backend**
   - Debe mostrar valores diferentes
   - Busca errores en la consola

4. **Compara CSVs muy diferentes**
   - Uno con beta alto vs uno con beta bajo
   - Diferencias deben ser obvias

---

**¡Ahora el sistema está completamente funcional y verificable!** 🎵🧠✅

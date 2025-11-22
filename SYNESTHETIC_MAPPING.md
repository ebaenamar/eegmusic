# 🎨 Mapeo Sinestésico EEG → Música

## 📊 Análisis de los Dos CSVs

### CSV 1 (Desktop - Más Activo)
- **Banda Dominante**: Theta (0.357)
- **Beta**: 0.285 (ALTO - más actividad motora)
- **Gamma**: 0.110 (ALTO - más complejidad)
- **Alpha/Beta**: 0.91 (equilibrado)
- **Low/High Freq**: 0.97 (balanceado)
- **Color**: 🟣 Púrpura brillante
- **Carácter**: Creativo, activo, complejo

### CSV 2 (Neurable - Más Relajado)
- **Banda Dominante**: Theta (0.594) - MUY ALTO
- **Beta**: 0.127 (BAJO - poca actividad motora)
- **Gamma**: 0.021 (MUY BAJO - simple)
- **Alpha/Beta**: 1.80 (más relajado)
- **Low/High Freq**: 4.31 (MUY espacioso)
- **Color**: 🟣 Púrpura oscuro
- **Carácter**: Meditativo, lento, espacioso

## 🎵 Diferencias Musicales Que DEBEN Notarse

### 1. TEMPO (Beta)
**CSV 1**: Beta = 0.285 → **100-110 BPM** (medio-rápido)
**CSV 2**: Beta = 0.127 → **70-80 BPM** (lento)
**Diferencia**: 30-40 BPM - ¡DEBE ser obvia!

### 2. DENSIDAD DE NOTAS (Beta + Gamma)
**CSV 1**: 
- Beta alto → 6-8 notas/segundo
- Gamma alto → Acordes complejos (7ª, 9ª)
- Resultado: **Música densa, rica**

**CSV 2**:
- Beta bajo → 2-3 notas/segundo  
- Gamma bajo → Acordes simples (tríadas)
- Resultado: **Música espaciosa, simple**

### 3. ESPACIALIDAD (Low/High Ratio)
**CSV 1**: Ratio = 0.97 → **Balanceado, lleno**
**CSV 2**: Ratio = 4.31 → **Espacioso, vacío, minimalista**

### 4. ARTICULACIÓN (Alpha)
**CSV 1**: Alpha = 0.218 → **Normal** (80% duración)
**CSV 2**: Alpha = 0.208 → **Normal** (80% duración)
**Diferencia**: Mínima - OK

### 5. COMPLEJIDAD ARMÓNICA (Gamma)
**CSV 1**: Gamma = 0.110 → **Acordes complejos**
- Usar 7ª, 9ª, suspensiones
- 5-6 acordes por progresión
- Modulaciones frecuentes

**CSV 2**: Gamma = 0.021 → **Acordes simples**
- Solo tríadas básicas
- 3-4 acordes por progresión
- Sin modulaciones

## 🎯 Implementación Necesaria

### Cambios Críticos:

#### 1. **Tempo Más Extremo**
```python
# Actual: tempo basado en arousal (0-1)
# Problema: Rango muy estrecho (80-120 BPM)

# Nuevo: tempo basado en Beta directamente
if beta > 0.35:
    tempo = 110 + (beta - 0.35) * 100  # 110-140 BPM
elif beta > 0.20:
    tempo = 90 + (beta - 0.20) * 133   # 90-110 BPM
else:
    tempo = 60 + beta * 150            # 60-90 BPM
```

#### 2. **Densidad Basada en Low/High Ratio**
```python
low_high_ratio = (delta + theta) / (beta + gamma + 0.01)

if low_high_ratio > 3.0:
    # Muy espacioso (CSV 2)
    notes_per_second = 1.5
    silence_probability = 0.3  # 30% silencios
    chord_density = 'sparse'   # Solo root + fifth
elif low_high_ratio > 1.5:
    # Balanceado
    notes_per_second = 4
    silence_probability = 0.1
    chord_density = 'normal'   # Tríadas
else:
    # Denso (CSV 1)
    notes_per_second = 8
    silence_probability = 0
    chord_density = 'rich'     # 7ª, 9ª, suspensiones
```

#### 3. **Complejidad Armónica Real (Gamma)**
```python
if gamma > 0.08:
    # Muy complejo
    chord_extensions = [7, 9, 11]  # 7ª, 9ª, 11ª
    num_chords = 5-6
    modulation_prob = 0.3
elif gamma > 0.04:
    # Moderado
    chord_extensions = [7]  # Solo 7ª
    num_chords = 4
    modulation_prob = 0.1
else:
    # Simple
    chord_extensions = []  # Solo tríadas
    num_chords = 3
    modulation_prob = 0
```

#### 4. **Silencios y Pausas (Low Freq)**
```python
# CSV 2 tiene mucho más theta/delta → más pausas
if (delta + theta) > 0.4:
    # Añadir silencios entre frases
    pause_duration = 0.5 * (delta + theta)
    pause_probability = 0.2
```

#### 5. **Timbre Basado en Frecuencias**
```python
# CSV 1: Gamma alto → Bright, sharp
if gamma > 0.08:
    harmonics = 5-7  # Muchos armónicos
    filter_cutoff = 8000  # Brillante
    
# CSV 2: Gamma bajo → Warm, dark
else:
    harmonics = 2-3  # Pocos armónicos
    filter_cutoff = 2000  # Oscuro
```

## 🎨 Resultado Sinestésico Esperado

### CSV 1 (Activo):
- 🎵 Tempo: 100-110 BPM (rápido)
- 🎹 Notas: 6-8/segundo (densas)
- 🎼 Acordes: Complejos (7ª, 9ª)
- 🔊 Timbre: Brillante, agudo
- 🎭 Carácter: **Activo, complejo, rico**
- 🎨 Color: Púrpura brillante con destellos

### CSV 2 (Relajado):
- 🎵 Tempo: 70-80 BPM (lento)
- 🎹 Notas: 2-3/segundo (espaciadas)
- 🎼 Acordes: Simples (tríadas)
- 🔊 Timbre: Oscuro, cálido
- 🎭 Carácter: **Meditativo, simple, espacioso**
- 🎨 Color: Púrpura oscuro con pausas

## ✅ Checklist de Implementación

- [ ] Tempo basado directamente en Beta (no arousal)
- [ ] Densidad de notas basada en Low/High ratio
- [ ] Silencios/pausas para estados de baja frecuencia
- [ ] Extensiones de acordes basadas en Gamma
- [ ] Número de acordes variable con Gamma
- [ ] Timbre (armónicos) basado en Gamma
- [ ] Volumen de cada capa basado en bandas
- [ ] Logs que muestren las características sinestésicas

## 🎯 Objetivo Final

**La diferencia debe ser TAN obvia que:**
1. CSV 1 suena como "café con actividad mental"
2. CSV 2 suena como "meditación profunda"
3. No hace falta ser músico para notar la diferencia
4. La música "pinta" el estado mental visualmente

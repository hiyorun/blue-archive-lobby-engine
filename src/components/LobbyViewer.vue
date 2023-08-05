<template>
    <div>
        <canvas id="screen"></canvas>
    </div>
</template>
  
<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import * as PIXI from 'pixi.js';
import { Spine } from 'pixi-spine';
import { useSettings } from '@/stores/settings';
import type { Animations } from '@/stores/settings';

const settings = useSettings();

let render: PIXI.Application | null = null;
let spineModel: Spine | null = null;
const isCharacterLoaded = ref(false);

// Call initCanvas on component mount
onMounted(initCanvas);

watch(
    [() => settings.fetchCurrentAnimation,
    () => settings.fetchLoop,
    ],
    () => applyAnimation(settings.fetchCurrentAnimation)
)
watch(
    () => settings.fetchCurrentModel,
    (v) => loadModel(v.path)
)


// Initialize PIXI application
function initCanvas() {
    render = new PIXI.Application({
        width: window.innerWidth,
        height: window.innerHeight,
        view: document.getElementById('screen') as HTMLCanvasElement,
    });
    loadModel(settings.fetchCurrentModel.path);
}

// Load spine model and handle loaded event
function loadModel(model: string) {

    isCharacterLoaded.value = false;
    // remove previous spine model
    if (render && render.stage.children.length > 0) {
        render.stage.children.pop();
        PIXI.Assets.reset
    }

    // load new spine model
    PIXI.Assets.load(model).then(onModelLoad);
}

// Handle assets loaded event
function onModelLoad(res: any) {
    spineModel = new Spine(res.spineData);

    // Scale
    spineModel.scale.x = 0.5;
    spineModel.scale.y = 0.5;

    // Centerize
    spineModel.x = window.innerWidth / 2;
    spineModel.y = window.innerHeight / 1;

    // Insert animations
    const animations: Animations[] = res.spineData.animations;
    settings.storeAnimations(animations);

    // Play Animation
    spineModel.state.setAnimation(0, "Idle_01", settings.fetchLoop);
    settings.setAnimation("Idle_01");

    // Add to main canvas
    if (render) {
        render.stage.addChild(spineModel);
    }
    isCharacterLoaded.value = true;
}

function applyAnimation(name: string) {
    if (spineModel) {
        spineModel.state.setAnimation(0, name, settings.fetchLoop);
    }
}
</script>

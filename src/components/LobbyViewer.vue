<!-- MyComponent.vue -->
<template>
    <div>
        <canvas id="screen"></canvas>
    </div>
</template>
  
<script setup>
import { ref, watch, onMounted } from 'vue';
import * as PIXI from 'pixi.js';
import { Spine } from 'pixi-spine';
import { useParams } from '@/stores/parameters.ts';
import { storeToRefs } from 'pinia';

const parameter = useParams();

let render = null;
let spineModel = null;
const isCharacterLoaded = ref(false);

// Call reCanvas on component mount
onMounted(reCanvas);
watch(
    () => parameter.fetchCurrentAnimation,
    () => applyAnimation()
)
watch(
    () => parameter.fetchChanges,
    () => {
        applyAnimation()
    }
)

// Initialize PIXI application
function reCanvas() {
    render = new PIXI.Application({
        width: window.innerWidth,
        height: window.innerHeight,
        view: document.getElementById('screen'),
    });
    loadModel()
}

// Load spine model and handle loaded event
function loadModel(model = 'models/aris_home/Aris_home.skel') {
    isCharacterLoaded.value = false;
    // remove previous spine model
    if (render.stage.children.length > 0) {
        render.stage.children.pop();
        PIXI.Assets.load.resources = {};
    }

    // load new spine model
    PIXI.Assets.load(model).then(onModelLoad);
}

// Handle assets loaded event
function onModelLoad(res) {
    spineModel = new Spine(res.spineData);

    // Scale
    spineModel.scale.x = 0.5;
    spineModel.scale.y = 0.5;

    // Centerize
    spineModel.x = window.innerWidth / 2;
    spineModel.y = window.innerHeight / 1;

    // Insert animations
    const animations = res.spineData.animations;
    parameter.storeAnimations(animations)

    // Play Animation
    spineModel.state.setAnimation(0, animations[0].name, parameter.isLoop);
    parameter.setAnimation(animations[0].name)

    // Add to main canvas
    render.stage.addChild(spineModel);
    isCharacterLoaded.value = true;
}

function applyAnimation() {
    name = parameter.fetchCurrentAnimation
    console.log(parameter.isLoop)
    spineModel.state.setAnimation(0, name, parameter.isLoop);
}


</script>
  
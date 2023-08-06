<template>
    <div>
        <div @click="debuggerButton()" class=" rounded-full bg-arisu-200 dark:bg-arisu-900 absolute left-12 m-2 p-2 text-arisu-600
            dark:text-arisu-400 cursor-pointer">
            <span>Debug Spine</span>
        </div>
        <canvas @mousedown="deployHeadPats" @mouseup="releaseHeadPat" id="screen"></canvas>
    </div>
</template>
  
<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import * as PIXI from 'pixi.js';
import { Spine, type IBone } from 'pixi-spine';
import { useSettings } from '@/stores/settings';
import type { Animations } from '@/stores/settings';

const settings = useSettings();

interface headpatRange {
    centerX: number;
    centerY: number;
    initialY: number
}

let touchRange: headpatRange

let canvas: HTMLCanvasElement | null = null;
let render: PIXI.Application | null = null;
let spineModel: Spine | null = null;
let touchPoint: IBone | null = null;
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

function debuggerButton(): void {
}

// Initialize PIXI application
function initCanvas(): void {
    canvas = document.getElementById('screen') as HTMLCanvasElement
    render = new PIXI.Application({
        width: window.innerWidth,
        height: window.innerHeight,
        view: canvas
    });
    loadModel(settings.fetchCurrentModel.path);
    window.addEventListener('resize', (e) => {
        console.log(e)
        resizeCanvas(), 2000
    }, true);
}

// Load spine model and handle loaded event
function loadModel(model: string): void {

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
function onModelLoad(res: any): void {
    spineModel = new Spine(res.spineData);

    changeScale()

    // Insert animations
    const animations: Animations[] = res.spineData.animations;
    settings.storeAnimations(animations);

    // Play Animation
    spineModel.state.setAnimation(0, "Idle_01", settings.fetchLoop);
    spineModel.state.setAnimation(1, "Dummy", settings.fetchLoop);
    spineModel.state.setAnimation(2, "Dummy", settings.fetchLoop);

    settings.setAnimation("Idle_01");

    // Add to main canvas
    if (render) {
        render.stage.addChild(spineModel);
    }
    isCharacterLoaded.value = true;
}

function resizeCanvas(): void {
    if (!canvas || !render) {
        return
    }

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    render.resizeTo = canvas as HTMLElement

    changeScale()
}

function changeScale(scale: number = window.innerWidth / 4000, x: number = window.innerWidth / 2, y: number = window.innerHeight): void {
    if (!spineModel) {
        return
    }
    // Scale
    spineModel.scale.x = scale;
    spineModel.scale.y = scale;

    // Centerize
    spineModel.x = x;
    spineModel.y = y;

    defineTouchPoint()
}

function defineTouchPoint(): void {
    if (!spineModel) {
        return
    }
    touchPoint = spineModel.skeleton.findBone("Touch_Point")
    //@ts-ignore
    touchPoint.updateWorldTransform()
    //@ts-ignore
    const x = touchPoint.worldX * spineModel.scale.x + window.innerWidth / 2
    //@ts-ignore
    const y = touchPoint.worldY * spineModel.scale.y + window.innerHeight
    touchRange = {
        centerX: x,
        centerY: y,
        //@ts-ignore
        initialY: touchPoint.y
    }
}

function deployHeadPats(event: MouseEvent): void {
    if (event.clientX < touchRange.centerX - 100 || event.clientX > touchRange.centerX + 100) {
        return
    }
    if (event.clientY < touchRange.centerY - 100 || event.clientY > touchRange.centerY + 100) {
        return
    }
    canvas?.addEventListener("pointermove", doRotation)
    if (!spineModel || settings.fetchCurrentAnimation !== "Idle_01") {
        return
    }
    console.log("Deploying headpats")

    spineModel.stateData.setMix("Dummy", "Pat_01_M", 0.1)
    spineModel.stateData.setMix("Dummy", "Pat_01_A", 0.1)
    spineModel.state.setAnimation(1, "Pat_01_A", false)
    spineModel.state.setAnimation(2, "Pat_01_M", false)
}

function releaseHeadPat(): void {
    canvas?.removeEventListener("pointermove", doRotation)
    if (!spineModel || !touchPoint || settings.fetchCurrentAnimation !== "Idle_01") {
        return
    }
    console.log("Headpat released")

    spineModel.stateData.setMix("Pat_01_M", "Dummy", 0.1)
    spineModel.stateData.setMix("Pat_01_A", "Dummy", 0.1)
    spineModel.state.setAnimation(1, "Dummy", settings.fetchLoop);
    spineModel.state.setAnimation(2, "Dummy", settings.fetchLoop);
    //@ts-ignore
    touchPoint.y = touchRange.initialY
}

// Function to check if the cursor is on the left or right side of the line
function checkCursorSide(cursorX: number, cursorY: number, rotation: number): number {
    const centerX = touchRange.centerX;
    const centerY = touchRange.centerY;

    // Calculate the coordinates of the imaginary line
    const slope = Math.tan(rotation * (Math.PI / 180));
    const lineY = slope * (cursorX - centerX) + centerY;
    if (slope < 0) {
        return cursorY - lineY
    }
    return lineY - cursorY
}

function doRotation(event: PointerEvent): void {
    if (!touchPoint) {
        console.error("Touch point is undefined or null")
        return
    }
    //@ts-ignore
    const cursorPos = checkCursorSide(event.clientX, event.clientY, touchPoint.getWorldRotationX())
    const maxHeadpat = 70

    if (cursorPos < 0) {
        //@ts-ignore
        touchPoint.y = touchRange.initialY + maxHeadpat * mapCursorValue(cursorPos)
        return
    }
    //@ts-ignore
    touchPoint.y = touchRange.initialY - maxHeadpat * mapCursorValue(cursorPos)
}

function mapCursorValue(cursorValue: number): number {
    if (cursorValue > 0) {
        cursorValue = -cursorValue
    }
    const scaleFactor = 0.001; // Adjust this value to control the increment rate
    const scaledValue = cursorValue * scaleFactor;
    const mappedValue = Math.exp(scaledValue) - 1; // Subtract 1 to avoid outputting negative values
    return Math.sign(cursorValue) * mappedValue;
}

function applyAnimation(name: string): void {
    if (spineModel) {
        spineModel.state.setAnimation(0, name, settings.fetchLoop);
    }
}
</script>

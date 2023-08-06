import { defineStore } from "pinia";

export interface Animations {
    duration: number;
    name: string;
    timelineIds: [];
    timelines: [];
}

interface XY {
    x: number;
    y: number;
}

interface Model {
    name: string
    path: string
}

export interface SettingsState {
    models: Model[]
    currentModel: Model;
    animations: Animations[];
    currentAnimation: string;
    loop: boolean;
    fit: string;
    scale: number;
    coordinate: XY
    FPS: number;
};

export const useSettings = defineStore({
    id: "settings",
    state: () => ({
        models: [{
            name: "",
            path: ""
        }],
        currentModel: {
            "name": "Kazusa",
            "path": "models/kazusa_home/kazusa_home.skel"
        },
        animations: [],
        currentAnimation: "",
        loop: true,
        fit: "",
        scale: 0,
        coordinate: {
            x: 0,
            y: 0,
        },
        FPS: 0,
    } as SettingsState),
    getters: {
        fetchAnimations(): Animations[] {
            return this.animations;
        },
        fetchCurrentAnimation(): string {
            return this.currentAnimation;
        },
        fetchLoop(): boolean {
            return this.loop;
        },
        fetchModels(): Model[] {
            return this.models
        },
        fetchCurrentModel(): Model {
            return this.currentModel
        }
    },
    actions: {
        storeAnimations(animations: Animations[]) {
            this.animations = animations;
        },
        storeModels(models: Model[]) {
            this.models = models
        },
        setModel(model: Model) {
            this.currentModel = model
        },
        setAnimation(name: string) {
            this.currentAnimation = name;
        },
        setLoop(truthy: boolean) {
            this.loop = truthy;
        },
        setFit() {
        },
        setScale() {
        },
        setXY() {
        },
        setFPS() {
        },
    },
});

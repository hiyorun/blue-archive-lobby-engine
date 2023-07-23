import { defineStore } from "pinia";

type Animation = {
    duration: number,
    name: string,
    timelineIds: [],
    timelines: [],
}

export type ParamState = {
    params: {
        character: string,
        animations: Animation[],
        currentAnimation: string,
        loop: boolean,
        fit: string,
        scale: number,
        x: number,
        y: number,
        FPS: number,
        date: number,
    }
}

export const useParams = defineStore({
    id: "parameter",
    state: () => ({
        params: {}
    } as ParamState),
    getters: {
        fetchParameters(): ParamState {
            return this.params
        },
        fetchChanges(): number {
            return this.params.date
        },
        fetchCurrentAnimation(): string {
            return this.params.currentAnimation
        },
        isLoop(): boolean {
            return this.params.loop;
        },
    },
    actions: {
        storeAnimations(animation: Animation) {
            this.params.animations = animation
        },
        setCharacter() {
            this.params.date = Date.now()
        },
        setAnimation(name: string) {
            this.params.currentAnimation = name
            this.params.date = Date.now()
        },
        setLoop(truthy: boolean) {
            this.params.loop = truthy
            this.params.date = Date.now()
        },
        setFit() {
            this.params.date = Date.now()
        },
        setScale() {
            this.params.date = Date.now()
        },
        setXY() {
            this.params.date = Date.now()
        },
        setFPS() {
            this.params.date = Date.now()
        },
    },
});

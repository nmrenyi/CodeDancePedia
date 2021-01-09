<template>
    <div class="contain" ref="container"></div>
</template>

<script>
import * as THREE from 'three'

export default {
    name: "Canvas",
    data(){
        return{
            width: 0,
            height: 0,
        }
    },
    mounted(){
        this.$nextTick(() => {
            this.CanvasRender()
        });

        window.onresize = () => {
            return (() => {
                var container = this.$refs.container;
                this.width = container.clientWidth;
                this.height = container.clientHeight;
            })();
        };
    },

    methods:{
        CanvasRender(){
            var container = this.$refs.container;
            this.width = container.clientWidth;
            this.height = container.clientHeight;
            var renderer = new THREE.WebGLRenderer();
            // var renderer = new THREE.CanvasRenderer();
            renderer.setSize(this.width, this.height);
            console.log("当前窗口大小输出：", this.width, " ", this.height)
            container.appendChild(renderer.domElement);

            var scene = new THREE.Scene();

            var system = new THREE.Group(); // planetary system

            scene.add(
            new THREE.AmbientLight(0xFFFFFF, 0.2)
            );

            var light = new THREE.DirectionalLight(0xFFFFFF, 2.5);
            light.position.set(1500, 2500, 0);
            scene.add(light);

            var material = new THREE.MeshLambertMaterial({
            color: 0x0C2D4D
            });

            var planet = new THREE.Mesh(
            new THREE.IcosahedronGeometry(100, 3),
            material
            );

            for (var i = 0; i < planet.geometry.vertices.length; i++){
                planet.geometry.vertices[i].multiplyScalar(
                    Math.random() * 0.05 + 0.95
                );
            }

            planet.geometry.computeFlatVertexNormals();
            system.add(planet);

            var asteroids = new THREE.Group();

            for (var p = 0; p < Math.PI * 2; p = p + Math.random() * 0.15) {
            var asteroid = new THREE.Mesh(
                new THREE.IcosahedronGeometry(8, 0),
                material
            );

            var size = Math.random() * 0.5;
            for (i = 0; i < asteroid.geometry.vertices.length; i++){
                asteroid.geometry.vertices[i].multiplyScalar(
                Math.random() * 0.5 + size
                );
            }

            var rand = Math.random() * 60 - 30;
            asteroid.position.set(200 * Math.sin(p) + rand, rand, 200 * Math.cos(p) + rand);

            asteroid.geometry.computeFlatVertexNormals();
            asteroids.add(asteroid);
            }

            system.add(asteroids);

            system.rotation.x = 0.1;
            system.rotation.y = -.3;
            system.rotation.z = -0.4;

            scene.add(system);

            for (i = 0; i < 10; i++) {
            var particles = new THREE.Points(
                new THREE.Geometry(),
                new THREE.PointsMaterial({
                size: Math.random() * 5
                })
            );
            for (var j = 0; j < 20; j++) {
                var vertex = new THREE.Vector3();
                vertex.x = Math.random() * this.width * 1.1 - this.width * 1.1 / 2;
                vertex.y = Math.random() * this.height * 1.1 - this.height * 1.1 / 2;
                vertex.z = -500;
                particles.geometry.vertices.push(vertex);
                particles.material.color.setScalar(Math.random() * 0.4 + 0.2);
            }
            scene.add(particles);
            }

            var camera_z = 450

            function render() {
                requestAnimationFrame(render);

                planet.rotation.y += 0.001;
                planet.rotation.z -= 0.0005;

                asteroids.rotation.y += 0.003;

                var width = container.clientWidth;
                var height = container.clientHeight;
                renderer.setSize(width, height);

                var aspect = width / height;
                var camera = new THREE.PerspectiveCamera(50, aspect, 0.1, 1000);
                camera.position.z = camera_z
                if(camera_z > 380){
                    camera_z -= 0.008
                }

                renderer.render(scene, camera);
            }

            render();
        }
    },
}
</script>

<style>
    * {
        margin: 0;
        padding: 0;
        outline: 0;
    }
    div.contain {
        width: 100%;
        height: 100%;
        position: fixed;
        z-index: 0;
    }  
</style>
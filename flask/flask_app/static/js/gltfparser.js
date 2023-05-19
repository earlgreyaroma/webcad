import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// get GLTF object
async function getGLTF() {
  getFromFlask(
    '/get_gltf', 
    function(response) {
    console.log(response)
    return response
  });
}



// POST function for variable values
function postVar(param, value) {
  postToFlask(
    '/process_var', 
    {
      "var": param, 
      "value": value
    }, 
    function(response) {
      console.log(response)
      render()
  });
}

function renderGLTF(gltfJSON) {

  // set scene
  const scene = new THREE.Scene();


  // get Sizes
  const column = document.querySelector('#webgl-col');
  const columnRect = column.getBoundingClientRect();
  const colHeight = columnRect.height;
  const colWidth = columnRect.width;
  const aspectRatio = colWidth / colHeight;


  // load GLTF object
  let size;
  const GltfLoader = new GLTFLoader();
  GltfLoader.parse(
    gltfJSON,
    '',
    function(gltf) {
      scene.add(gltf.scene);
      gltf.animations;
      gltf.scene;
      gltf.scenes;
      gltf.cameras;
      gltf.asset;

      // get gltf model size
      const box = new THREE.Box3().setFromObject( gltf.scene); 
      const size3D = box.getSize(new THREE.Vector3());
      size = Math.max(size3D.x, size3D.y, size3D.z) * 1.5;

      // update camera
      camera.left = size * aspectRatio / -2;
      camera.right = size * aspectRatio / 2;
      camera.top = size / 2;
      camera.bottom = size / -2;
      camera.updateProjectionMatrix();
    },
    function(error) {console.log('error occured!!!')}
  );


  // set camera
  const camera = new THREE.OrthographicCamera( size * aspectRatio / -2, size * aspectRatio / 2, size / 2, size / - 2, 0.01, 200);
  camera.position.set(1, 1, 1);
  scene.add(camera);


  // set renderer
  const canvas = document.querySelector('#webgl-can');
  const renderer = new THREE.WebGLRenderer({ canvas });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(colWidth , colHeight);
  renderer.render(scene, camera);


  // set lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
  scene.add(ambientLight);
  const spotLight1 = new THREE.SpotLight(0xffffff, 0.5);
  spotLight1.position.set(10, 5, 1);
  scene.add(spotLight1);
  const spotLight2 = new THREE.SpotLight(0xffffff, 0.2);
  spotLight2.position.set(-1, -1, -5);
  scene.add(spotLight2);

  // set background
  const bgcolor = new THREE.Color(0xffffff);
  scene.background = bgcolor;


  // set mouse controls
  const controls = new OrbitControls(camera, renderer.domElement);


  // checks if window is resized
  window.addEventListener('resize', onWindowResize, false);


  // resize function
  function onWindowResize() {

    // update sizes
    const newColumnRect = column.getBoundingClientRect();
    const newColHeight = newColumnRect.height;
    const newColWidth = newColumnRect.width;
    const newAspectRatio = newColWidth / newColHeight;

    // update camera
    camera.left = size * newAspectRatio / -2;
    camera.right = size * newAspectRatio / 2;
    camera.top = size / 2;
    camera.bottom = size / -2;
    camera.updateProjectionMatrix();

    // update renderer
    renderer.setSize(newColWidth, newColHeight);
  }

  // animation loop
  function animate() {
    requestAnimationFrame( animate );
    controls.update();
    renderer.render(scene, camera);
  }

  animate();
}

async function render() {
  let gltfJSON = await getGLTF()
  console.log(gltfJSON)
  renderGLTF(gltfJSON);
}


// Get all range input elements
var ranges = document.querySelectorAll('input[type="range"]');

// Add event listeners to each range input element
ranges.forEach(function(range) {
  range.addEventListener('input', function() {
    // Get the values of the selected range
    var value = this.value;

    // Update the current value display
    var currentValue = this.parentNode.parentNode.querySelector('.value');
    currentValue.textContent = value;
  });
});


// Add event listeners to each range change element
ranges.forEach(function(range) {
  range.addEventListener('change', function() {
    // Get the value and ID of the selected range
    var value = this.value;
    var id = this.id;
    postVar(id,value);
  });
});


render();





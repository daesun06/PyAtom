import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

interface AtomicModelProps {
  protons: number;
  neutrons: number;
  electronShells: number[];
}

// Nucleus component containing protons and neutrons
function Nucleus({ protons, neutrons }: { protons: number; neutrons: number }) {
  const nucleusRef = useRef<THREE.Group>(null);
  
  const nucleons = useMemo(() => {
    const items: { type: 'proton' | 'neutron'; position: THREE.Vector3 }[] = [];
    const total = protons + neutrons;
    
    // Create nucleons in a clustered arrangement using golden ratio sphere packing
    for (let i = 0; i < total; i++) {
      const type = i < protons ? 'proton' : 'neutron';
      
      if (i === 0) {
        items.push({ type, position: new THREE.Vector3(0, 0, 0) });
      } else {
        const goldenRatio = (1 + Math.sqrt(5)) / 2;
        const theta = 2 * Math.PI * i / goldenRatio;
        const phi = Math.acos(1 - 2 * (i + 0.5) / total);
        
        // Use deterministic pseudo-random based on index for stable results
        const r = 0.5 + (Math.sin(i * 12.9898) * 43758.5453 % 1) * 0.3 + 0.15;
        const x = r * Math.sin(phi) * Math.cos(theta);
        const y = r * Math.sin(phi) * Math.sin(theta);
        const z = r * Math.cos(phi);
        
        items.push({ type, position: new THREE.Vector3(x, y, z) });
      }
    }
    
    return items;
  }, [protons, neutrons]);
  
  useFrame((state) => {
    if (nucleusRef.current) {
      nucleusRef.current.rotation.y = state.clock.elapsedTime * 0.5;
      nucleusRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.2;
    }
  });
  
  return (
    <group ref={nucleusRef}>
      {nucleons.map((nucleon, index) => (
        <mesh key={index} position={nucleon.position}>
          <sphereGeometry args={[0.25, 16, 16]} />
          <meshStandardMaterial 
            color={nucleon.type === 'proton' ? '#ef4444' : '#22c55e'} 
            roughness={0.3}
            metalness={0.4}
          />
        </mesh>
      ))}
    </group>
  );
}

// Electron shell component
function ElectronShell({ 
  shellIndex, 
  electronCount, 
  radius 
}: { 
  shellIndex: number; 
  electronCount: number; 
  radius: number;
}) {
  const shellRef = useRef<THREE.Group>(null);
  const electronsRef = useRef<THREE.Group>(null);
  
  // Calculate electron positions evenly distributed around the ring
  const electronPositions = useMemo(() => {
    const positions: THREE.Vector3[] = [];
    for (let i = 0; i < electronCount; i++) {
      const angle = (i / electronCount) * Math.PI * 2;
      positions.push(new THREE.Vector3(
        Math.cos(angle) * radius,
        0,
        Math.sin(angle) * radius
      ));
    }
    return positions;
  }, [electronCount, radius]);
  
  // Rotation speed: inner shells rotate faster
  const rotationSpeed = useMemo(() => 1 / (shellIndex + 1) * 2 + 0.5, [shellIndex]);
  
  useFrame((state) => {
    if (electronsRef.current) {
      electronsRef.current.rotation.y = state.clock.elapsedTime * rotationSpeed;
    }
    if (shellRef.current) {
      // Slight tilt to each shell for 3D effect
      shellRef.current.rotation.x = shellIndex * 0.3;
      shellRef.current.rotation.z = shellIndex * 0.2;
    }
  });
  
  return (
    <group ref={shellRef}>
      {/* Orbit ring */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[radius, 0.02, 8, 64]} />
        <meshStandardMaterial color="#94a3b8" transparent opacity={0.4} />
      </mesh>
      
      {/* Electrons */}
      <group ref={electronsRef}>
        {electronPositions.map((position, index) => (
          <mesh key={index} position={position}>
            <sphereGeometry args={[0.12, 12, 12]} />
            <meshStandardMaterial 
              color="#3b82f6" 
              emissive="#1d4ed8"
              emissiveIntensity={0.5}
              roughness={0.2}
              metalness={0.6}
            />
          </mesh>
        ))}
      </group>
    </group>
  );
}

// Main atom component
function Atom({ protons, neutrons, electronShells }: AtomicModelProps) {
  const atomRef = useRef<THREE.Group>(null);
  
  useFrame((state) => {
    if (atomRef.current) {
      // Slow overall rotation for 3D effect
      atomRef.current.rotation.y = state.clock.elapsedTime * 0.1;
      atomRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.1) * 0.1;
    }
  });
  
  // Calculate shell radii
  const shellRadii = useMemo(() => {
    return electronShells.map((_, index) => 1.5 + index * 1.2);
  }, [electronShells]);
  
  return (
    <group ref={atomRef}>
      {/* Nucleus */}
      <Nucleus protons={protons} neutrons={neutrons} />
      
      {/* Electron shells */}
      {electronShells.map((electronCount, index) => (
        <ElectronShell 
          key={index}
          shellIndex={index}
          electronCount={electronCount}
          radius={shellRadii[index]}
        />
      ))}
    </group>
  );
}

// Main component
export default function AtomicModel({ protons, neutrons, electronShells }: AtomicModelProps) {
  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <Canvas
        camera={{ position: [0, 0, 10], fov: 45 }}
        style={{ background: 'linear-gradient(to bottom, #0f172a, #1e293b)' }}
      >
        {/* Ambient light */}
        <ambientLight intensity={0.4} />
        
        {/* Directional light */}
        <directionalLight 
          position={[10, 10, 5]} 
          intensity={1} 
          castShadow
        />
        
        {/* Additional lighting for better visibility */}
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#60a5fa" />
        <pointLight position={[10, -10, 10]} intensity={0.3} color="#f472b6" />
        
        {/* Atom model */}
        <Atom 
          protons={protons} 
          neutrons={neutrons} 
          electronShells={electronShells} 
        />
        
        {/* Orbit controls for user interaction */}
        <OrbitControls 
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={3}
          maxDistance={20}
        />
      </Canvas>
    </div>
  );
}

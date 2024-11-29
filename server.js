const express = require('express');
const { ethers } = require('ethers');
const path = require('path');
const swaggerJsDoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');
require('dotenv').config();

// Debugging: Log current directory
console.log('Current working directory:', __dirname);

// Load environment variables
const API_URL = process.env.API_URL;
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;

if (!API_URL || !PRIVATE_KEY || !CONTRACT_ADDRESS) {
    throw new Error('Please define API_URL, PRIVATE_KEY, and CONTRACT_ADDRESS in the .env file.');
}

// Load the compiled contract ABI
const { abi } = require('./artifacts/contracts/Contract.sol/ParkingFeeSystem.json');

// Blockchain setup
const provider = new ethers.providers.JsonRpcProvider(API_URL);
const signer = new ethers.Wallet(PRIVATE_KEY, provider);
const contract = new ethers.Contract(CONTRACT_ADDRESS, abi, signer);

// Swagger setup
const swaggerOptions = {
    swaggerDefinition: {
        openapi: '3.0.0',
        info: {
            title: 'Parking Fee System API',
            version: '1.0.0',
            description: 'API for managing parking fee system using Ethereum smart contracts.',
        },
        servers: [
            {
                url: 'http://localhost:3000',
                description: 'Local server',
            },
        ],
    },
    apis: ['./server.js'], // Path to the API docs in this file
};

const swaggerDocs = swaggerJsDoc(swaggerOptions);

// Express app setup
const app = express();
app.use(express.json());
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// Swagger API Documentation
/**
 * @swagger
 * components:
 *   schemas:
 *     Vehicle:
 *       type: object
 *       properties:
 *         vehicleNumber:
 *           type: string
 *           description: The vehicle number
 *         userName:
 *           type: string
 *           description: The name of the vehicle owner
 *       required:
 *         - vehicleNumber
 *         - userName
 */

/**
 * @swagger
 * /registerVehicle:
 *   post:
 *     summary: Register a new vehicle
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Vehicle'
 *     responses:
 *       200:
 *         description: Vehicle registered successfully
 *       400:
 *         description: Bad request
 *       500:
 *         description: Internal server error
 */

// Register a vehicle
app.post('/registerVehicle', async (req, res) => {
    const { vehicleNumber, userName } = req.body;

    if (!vehicleNumber || !userName) {
        return res.status(400).json({ error: 'Vehicle number and user name are required.' });
    }

    try {
        console.log('Registering vehicle:', { vehicleNumber, userName });

        const tx = await contract.registerVehicle(vehicleNumber, userName, {
            gasLimit: 300000,
        });
        await tx.wait();

        res.status(200).json({ message: 'Vehicle registered successfully.' });
    } catch (error) {
        console.error('Transaction failed:', error);

        if (error.data) {
            const reason = ethers.utils.toUtf8String('0x' + error.data.slice(138));
            console.error('Revert Reason:', reason);
            return res.status(500).json({ error: reason });
        }

        res.status(500).json({ error: error.message });
    }
});


/**
 * @swagger
 * /setParkingHours:
 *   post:
 *     summary: Set parking hours for a vehicle
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               parkingHours:
 *                 type: integer
 *                 description: Number of parking hours
 *     responses:
 *       200:
 *         description: Parking hours set successfully
 *       400:
 *         description: Bad request
 *       500:
 *         description: Internal server error
 */

// Set parking hours
app.post('/setParkingHours', async (req, res) => {
    const { parkingHours } = req.body;
    if (!parkingHours || parkingHours <= 0) {
        return res.status(400).json({ error: 'Valid parking hours are required.' });
    }

    try {
        const tx = await contract.setParkingHours(parkingHours);
        await tx.wait();
        res.status(200).json({ message: 'Parking hours set successfully.' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * @swagger
 * /payFee:
 *   post:
 *     summary: Pay parking fee
 *     responses:
 *       200:
 *         description: Parking fee paid successfully
 *       500:
 *         description: Internal server error
 */

// Pay parking fee
app.post('/payFee', async (req, res) => {
    try {
        const tx = await contract.payFee();
        await tx.wait();
        res.status(200).json({ message: 'Parking fee paid successfully.' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Additional endpoints omitted for brevity; you can add Swagger docs for all endpoints similarly.

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
    console.log(`Swagger docs available at http://localhost:${PORT}/api-docs`);
});

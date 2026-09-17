// =============================================================================
// CLIENT ROUTES - /api/clients
// =============================================================================

import { Router } from 'express';
import { ClientController } from '../controllers/client.controller';
import { authenticateToken } from '../middlewares/auth.middleware';
import { validateBody } from '../middlewares/validate.middleware';
import { CreateClientSchema } from '../infrastructure/validators/schemas';

const router = Router();

router.use(authenticateToken);

router.get('/', ClientController.listClients);
router.get('/:id', ClientController.getClientById);
router.post('/', validateBody(CreateClientSchema), ClientController.createClient);
router.put('/:id', validateBody(CreateClientSchema.partial()), ClientController.updateClient);

export default router;

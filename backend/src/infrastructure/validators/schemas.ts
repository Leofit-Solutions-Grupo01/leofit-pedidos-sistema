// =============================================================================
// VALIDATION SCHEMAS (ZOD) - LEOFIT INPUT SANITIZATION & SECURITY
// =============================================================================

import { z } from 'zod';

export const LoginSchema = z.object({
  email: z.string().email('Email inválido').max(150),
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres').max(100)
});

export const RegisterUserSchema = z.object({
  name: z.string().min(2, 'El nombre es obligatorio').max(100),
  email: z.string().email('Email inválido').max(150),
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres').max(100),
  role: z.enum(['ADMIN', 'OPERATOR']).default('OPERATOR')
});

export const CreateCategorySchema = z.object({
  name: z.string().min(2).max(60),
  description: z.string().max(255).optional()
});

export const CreateProductVariantSchema = z.object({
  size: z.enum(['S', 'M', 'L', 'XL', 'XXL', 'UNICA']),
  color: z.string().min(2).max(50),
  sku: z.string().min(3).max(50),
  stock: z.number().int().min(0),
  alertThreshold: z.number().int().min(0).default(3)
});

export const CreateProductSchema = z.object({
  categoryId: z.number().int().positive(),
  name: z.string().min(3).max(120),
  description: z.string().optional(),
  basePrice: z.number().positive(),
  imageUrl: z.string().url().optional().or(z.literal('')),
  isActive: z.boolean().default(true),
  variants: z.array(CreateProductVariantSchema).min(1, 'Debe incluir al menos una variante')
});

export const UpdateProductSchema = CreateProductSchema.partial();

export const CreateClientSchema = z.object({
  fullName: z.string().min(3).max(120),
  phone: z.string().min(7).max(20),
  address: z.string().min(5).max(255),
  district: z.string().min(2).max(80),
  reference: z.string().max(255).optional()
});

export const CreateOrderSchema = z.object({
  clientId: z.number().int().positive().optional(),
  clientData: CreateClientSchema.optional(),
  paymentMethod: z.enum(['YAPE', 'PLIN', 'TRANSFERENCIA', 'CONTRAENTREGA', 'EFECTIVO']),
  shippingCost: z.number().min(0).default(0),
  notes: z.string().max(500).optional(),
  items: z.array(
    z.object({
      variantId: z.number().int().positive(),
      quantity: z.number().int().positive(),
      unitPrice: z.number().positive()
    })
  ).min(1, 'El pedido debe contener al menos un producto')
}).refine(data => data.clientId || data.clientData, {
  message: 'Debe especificar clientId o clientData'
});

export const UpdateOrderStatusSchema = z.object({
  status: z.enum(['RECIBIDO', 'PREPARACION', 'EN_CAMINO', 'ENTREGADO', 'CANCELADO']),
  comments: z.string().max(255).optional()
});

export const StockUpdateSchema = z.object({
  quantityDelta: z.number().int()
});
